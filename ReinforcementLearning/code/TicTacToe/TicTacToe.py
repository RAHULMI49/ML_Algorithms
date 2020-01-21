"""
Script for generating all the possible states of n * n tic tac toe game
"""

import numpy as np
import pandas as pd
import copy
import json


def load_data(filename):
    with open('%s' % (filename), 'r') as f:
        distros_dict = json.load(f)
    return distros_dict


class TicTacToe:
    def __init__(self, n, win_condition, first_player_symbol='X'):
        """ Generates the board
        """

        self.board = {'X': [], 'O': []}
        self.moves_mapping = {'X': 'O', 'O': 'X'}
        self.next_move = first_player_symbol
        self.win_condition = win_condition
        self.last_move_pos = -1
        self.board_length = n
        self.possible_move_positions = list(
            range(1, (self.board_length * self.board_length) + 1))

    def print_board(self):
        """Prints the board state in a matrix
        """
        board = np.empty((self.board_length, self.board_length), dtype = '<U10')
        for i in range(0, self.board_length):
            for j in range(0, self.board_length):
                board[i, j] = str(self.get_cell_number(i, j))
        board = self.fill_board(board, self.board['X'], 'X')
        board = self.fill_board(board, self.board['O'], 'O')
        print(pd.DataFrame(board))

    def fill_board(self, board, positions, symbol):
        """create a matrix of the current board state
        """
        for pos in positions:
            i, j = self.get_cell_indices(pos)
            board[i, j] = symbol
        return board

    def make_move(self, pos, symbol):
        """ updates the state in all the variables

        Returns
        =======
            tuple : 
                structure : (first_element, second_element)
                first_element : bool
                    status about the move, True if all conditions good, False otherwise
                second_element : tuple

        1. checks if the symbol is the correct for the next move
        2. checks if the position entered is the valid for the next move
        3. updates the position in the board
        4. updates the posibble move position
        5. updates the last move position
        6. updates the next move symbol
        7. checks the game status whether won or draw or none
        8. return the status of the move
        """
        assert (self.next_move == symbol)
        if pos in self.possible_move_positions:
            self.board[symbol].append(pos)

            self.possible_move_positions.remove(pos)
            self.last_move_pos = pos
            self.next_move = self.moves_mapping[symbol]

            status = self.check_complete(symbol)
            return True, status

        else:
            return (False, ("wrong move position", self.possible_move_positions))

    def get_state(self, board):
        """ generates the state as required by learning agent
        """
        xstate = '-'.join([str(xpos) for xpos in sorted(board['X'])])
        ystate = '-'.join([str(ypos) for ypos in sorted(board['O'])])
        return '|'.join([xstate, ystate])

    def get_cell_number(self, i, j):
        cell_number = j + (i * self.board_length) + 1
        return cell_number

    def get_cell_indices(self, cell_number):
        i, j = divmod(cell_number - 1, self.board_length)
        return (i, j)

    def check_valid(self, i, j):
        if i >= 0 and i < self.board_length and j >= 0 and j < self.board_length:
            return True
        else:
            return False

    def check_won(self, symbol, last_move_pos, board):
        """Based on the last move position the 
        pattern of that symbol is checked diagonally , vertically and horizontally
        """
        steps = [[1, 0], [0, 1], [1, 1], [1, -1]]
        for x_step, y_step in steps:
            directions = [-1, 1]
            count = 1
            last_i, last_j = self.get_cell_indices(last_move_pos)
            for direction in directions:
                curr_i, curr_j = (last_i + direction *
                                  x_step), (last_j + direction*y_step)
                if not self.check_valid(curr_i, curr_j):
                    continue
                last_position = self.get_cell_number(curr_i, curr_j)
                while last_position in board[symbol]:
                    count += 1
                    curr_i, curr_j = (curr_i + direction *
                                      x_step), (curr_j + direction*y_step)
                    if not self.check_valid(curr_i, curr_j):
                        break
                    last_position = self.get_cell_number(curr_i, curr_j)

            if count >= self.win_condition:
                return True
        return False

    def check_complete(self, symbol):
        """ Check if the game is complete or still continue
        """
        if self.check_won(symbol, self.last_move_pos, self.board):
            return True, (1, symbol, 'won')
        elif len(self.possible_move_positions) == 0:
            return True, (0.5, 'draw')
        else:
            return False, ()

    def ask_for_move(self):
        """ Ask the next player for the move
        """
        self.print_board()
        print("Turn of Player : %s" % (self.next_move))
        return self.next_move


if __name__ == "__main__":

    # board_length = 3
    # winning_condition = 3
    # game = TicTacToe(board_length, winning_condition)

    # a = game.generate_all_possible_states(game.possible_move_positions, {'X' : [], 'O' : []}, next_symbol= 'X')
    # b = game.generate_all_possible_states(game.possible_move_positions, {'X' : [], 'O' : []}, next_symbol= 'O')
    # a.update(b)
    # print (len(a))

    from .LearningAgent import LearningAgent
    
    def get_current_state_possible_states_n_moves(possible_moves, symbol, game):
        """ This function generates the possible states based on the possible moves
        """
        possible_states = {}
        win_states = []
        current_state = game.get_state(game.board)
        for move in possible_moves:
            board = copy.deepcopy(game.board)
            
            board[symbol].append(move)
            state = game.get_state(board)
            if game.check_won(symbol, move, board):
                win_states.append(state)
            possible_states.update({state: move})
        return possible_states, current_state, win_states

    board_length = 4
    winning_condition = 4
    game = TicTacToe(board_length, winning_condition, first_player_symbol='O')

    agent = LearningAgent(load_previous=load_data('../data/%s_%s/X_states.json' %
                                                  (board_length, winning_condition)))
    completed = False
    while not completed:

        symbol = game.next_move
        possible_moves = game.possible_move_positions
        if symbol == 'X':
            possible_states, current_state, win_states = get_current_state_possible_states_n_moves(
                possible_moves, 'X', game)
            for state in win_states:
                agent.set_state_value(state, 1)
            _, next_move = agent.make_move(
                current_state, possible_states, always_greedy=True)
            print("Agent runs : %s" % (next_move))
        else:
            symbol = game.ask_for_move()
            Input = input()
            next_move = int(Input)
        move_status, data = game.make_move(next_move, symbol)
        if move_status:
            # move sucessfull
            completed, result = data
            if completed:
                print(result)
                game.print_board()
        else:
            print(data)
            completed = True
