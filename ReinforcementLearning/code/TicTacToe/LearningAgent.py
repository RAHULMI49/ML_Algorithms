"""
Learning Agent for Tic Tac Toe based on Temporal Difference Technique
"""

import numpy as np
import random
import json

def load_data():
    with open('../X_states.json', 'r') as f:
        distros_dict = json.load(f)
    return distros_dict


class LearningAgent():
    """ This class represents the learning agent based on temporal difference
    """
    def __init__(self, states, eta=0.2, learing_rate=0.2, load_previous = False):
        """ Initialises the agent

        Parameters
        ==========
        states : dict 
            states of the agent to initialise with
        eta : float
            Exploration parameter
        learning_rate : float
            learning rate for the temporal difference
        load_previous : bool
            if True the states are initialised from the earlier saved states
        """
        self.eta = eta
        self.lr = learing_rate
        if load_previous:
            self.states = load_data()
        else:
            self.states = states

    def is_greedy_move(self):
        """ Samples 1 (for greedy) and 0 (for non greedy) from the binomial distribution
            with p = (1 - eta)
        """
        return np.random.binomial(1, 1 - self.eta)

    def choose_randomly(self, possible_moves):
        """ return a random move from list of moves
        """
        return random.choice(possible_moves)

    def update_state_value(self, old_state, new_state):
        """ this updates the old_state value based on the new_state value
            using temporal difference
        """
        new_value = self.states[old_state] + \
            self.lr * (self.states[new_state] - self.states[old_state])
        print ("new_value : %s"%(new_value))
        self.states[old_state] = new_value

    def make_move(self, current_state, next_possible_states, always_greedy = False):
        """ This function makes the move using the reinforcement algorithm

        Parameters
        ==========
        current_state : str
            the current state of the game
        next_possible_states : list
            each element represents the next possible state from here
        always_greedy : bool
            True only when playing, keep false while training

        """
        # getting type of the move to make - greedy or exploratory
        if not always_greedy:
            greedy_move = self.is_greedy_move()
        else:
            greedy_move = True
        
        ## reducing eta
        if not greedy_move:
            self.eta = 0.99 * self.eta

        # identifying possible greedy moves and exploratory moves
        encountered_states = {}
        score_state_tuple = []
        for state in next_possible_states:
            score = self.states[state]
            if score not in encountered_states:
                encountered_states.update({score: []})
            score_state_tuple.append((score, next_possible_states[state]))
            encountered_states[score].append(state)
        print ("current state : %s"%(current_state))
        print ("taking greedy move : %s" %(greedy_move))
        print ("score and moves : %s" %(str(score_state_tuple)))
        
        max_encountered = max(encountered_states.keys())

        # choosing the move
        if greedy_move:
            choose_from = encountered_states[max_encountered]
        else:
            choose_from = next_possible_states.keys()
        state = self.choose_randomly(list(choose_from))
        print ("chose : %s" %(next_possible_states[state]))

        return state, next_possible_states[state]