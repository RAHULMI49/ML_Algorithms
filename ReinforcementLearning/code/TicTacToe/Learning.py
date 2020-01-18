import copy
import json
from .TicTacToe import TicTacToe
from .LearningAgent import LearningAgent
import random
import sys
from time import time


def RandomMove(possible_moves):
    return random.choice(possible_moves)

def json_dump(data, filename):
    with open('../%s'%(filename), 'w') as outfile:
        json.dump(data, outfile)

def load_data(filename):
    with open('../%s'%(filename), 'r') as f:
        distros_dict = json.load(f)
    return distros_dict

def get_current_state_possible_states_n_moves(possible_moves, symbol, game):
    """ This function generates the possible states based on the possible moves
    """
    possible_states = {}
    current_state = game.get_state(game.board)
    for move in possible_moves:
        board = copy.deepcopy(game.board)
        board[symbol].append(move)
        possible_states.update({game.get_state(board): move})
    return possible_states, current_state


if __name__ == "__main__":
    board_length = 3
    winning_condition = 3
    game = TicTacToe(board_length, winning_condition)

    start = time()
    a = game.generate_all_possible_states(game.possible_move_positions, {'X' : [], 'O' : []}, next_symbol= 'X')
    b = game.generate_all_possible_states(game.possible_move_positions, {'X' : [], 'O' : []}, next_symbol= 'O')
    a.update(b)
    print ("time elapsed in generating initial states : %s" %(time() - start))

    X_initial_states = {}
    O_initial_states = {}
    for state, score in a.items():
        if score == 'X':
            X_initial_states.update({state : 1})
            O_initial_states.update({state : -1})
        elif score == 'O':
            X_initial_states.update({state : -1})
            O_initial_states.update({state : 1})
        else:
            X_initial_states.update({state : score})
            O_initial_states.update({state : score})

    # X_initial_states = load_data('X_states.json')
    # O_initial_states = load_data('Y_states.json')

    # print (X_initial_states['6-7-8|1-2-5'])
    # sys.exit()

    agent = LearningAgent(X_initial_states)
    agent2 = LearningAgent(O_initial_states)

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
            print ("===============\n")
            print ("%s turn" %(symbol))
            if symbol == 'X':
                possible_states, current_state = get_current_state_possible_states_n_moves(
                    possible_moves, 'X', game)
                new_state, next_move = agent.make_move(current_state, possible_states)
            else:
                possible_states, current_state = get_current_state_possible_states_n_moves(
                    possible_moves, 'O', game)
                new_state, next_move = agent2.make_move(current_state, possible_states)
                # next_move = RandomMove(possible_moves)
            agent.update_state_value(current_state, new_state)
            agent2.update_state_value(current_state, new_state)
            game.print_board()
            print ("================\n")
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
                    print ("draws : %s, X_wins : %s, O_wins : %s, prob_Xwins : %s" %(draws, X_wins, O_wins, round(X_wins/float(X_wins + O_wins), 2)))
                    print(result)
                    game.print_board()
                    print(len(agent.states))
                    print("================")
                    game = TicTacToe(board_length, winning_condition, first_player_symbol=random.choice(['X', 'O']))
            else:
                print(data)
                completed = True
    json_dump(agent.states, 'X_states.json')
    json_dump(agent2.states, 'Y_states.json')
    
