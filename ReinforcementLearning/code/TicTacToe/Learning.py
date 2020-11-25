import copy
import json
from .TicTacToe import TicTacToe
from .LearningAgent import LearningAgent
import random
import sys
import os
import shutil
from time import time


def RandomMove(possible_moves):
    return random.choice(possible_moves)


def json_dump(data, filename):
    with open('%s' % (filename), 'w') as outfile:
        json.dump(data, outfile)


def load_data(filename):
    with open('%s' % (filename), 'r') as f:
        distros_dict = json.load(f)
    return distros_dict


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


def make_dir(board_length, winning_condition):
    dir = '../data/%s_%s' % (board_length, winning_condition)
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    return dir


if __name__ == "__main__":
    board_length = 3
    winning_condition = 3
    game = TicTacToe(board_length, winning_condition)

    dir = make_dir(board_length, winning_condition)

    agent = LearningAgent()
    agent2 = LearningAgent()

    i = 0
    woncount = 0
    continous_won_count = 1000
    draws, X_wins, O_wins = 0, 0, 0
    while (i < 10000):
        i += 1
        completed = False
        while not completed:
            symbol = game.next_move
            possible_moves = game.possible_move_positions
            print("===============\n")
            print("%s turn" % (symbol))
            if symbol == 'X':
                possible_states, current_state, win_states = get_current_state_possible_states_n_moves(
                    possible_moves, 'X', game)
                for state in win_states:
                    agent.set_state_value(state, 1)
                    agent2.set_state_value(state, -1)
                new_state, next_move = agent.make_move(
                    current_state, possible_states)
            else:
                possible_states, current_state, win_states = get_current_state_possible_states_n_moves(
                    possible_moves, 'O', game)
                for state in win_states:
                    agent.set_state_value(state, -1)
                    agent2.set_state_value(state, 1)
                new_state, next_move = agent2.make_move(
                    current_state, possible_states)
                # next_move = RandomMove(possible_moves)

            game.print_board()
            print("================\n")
            move_status, data = game.make_move(int(next_move), symbol)
            if move_status:
                # move sucessfull
                completed, result = data
                if completed:
                    if result[0] == 1:
                        if result[1] == 'X':
                            woncount += 1
                            X_wins += 1
                        else:

                            O_wins += 1
                            woncount = 0
                    else:
                        draws += 1
                    print("draws : %s, X_wins : %s, O_wins : %s" % (
                        draws, X_wins, O_wins))
                    print(result)
                    game.print_board()
                    print(len(agent.states))
                    print("================")

                    game = TicTacToe(board_length, winning_condition,
                                     first_player_symbol=random.choice(['X', 'O']))
            else:
                print(data)
                completed = True

            agent.update_state_value(current_state, new_state)
            agent2.update_state_value(current_state, new_state)

            if i % 100 == 0:
                json_dump(dict(agent.states), '%s/X_states.json' % (dir))
                json_dump(dict(agent2.states), '%s/O_states.json' % (dir))
    json_dump(dict(agent.states), '%s/X_states.json' % (dir))
    json_dump(dict(agent2.states), '%s/O_states.json' % (dir))
