import random

import numpy as np
import os
import pickle
import copy


from board import Board, getHash
from settings import Settings


def makeAction(player, board: Board):
    available_actions = board.available_segments
    # if np.random.uniform(0, 1) <= player.exp_rate:
    #     return int(np.random.choice(len(available_actions), size=1)[0])
    value_max = -np.inf
    next_board_available_actions = copy.deepcopy(board.available_segments)
    equipotent_actions = []
    for a in available_actions:
        if board.getRewardWithSegment(a) >= 1 and len(set([segment._id for segment in next_board_available_actions])&set(a.neighbours_ids)) != 1:
            return available_actions.index(a)
        new_available_segments = [segment for segment in next_board_available_actions if segment._id != a._id]
        next_board_hash = getHash(new_available_segments, player.score)
        if player.states_value.get(next_board_hash) is None:
            value = 0.5
        else:
            value = player.states_value[next_board_hash]
            if Settings.VERBOSE_PLAYER:
                print("greedy action {} - value {}".format(a._id, value))
        if value > value_max:
            value_max = value
            equipotent_actions.clear()
            equipotent_actions.append(a)
        elif value == value_max:
            equipotent_actions.append(a)
    next_action = random.choice(equipotent_actions)
    if Settings.VERBOSE_PLAYER:
        print("CHOSEN greedy action {} - value {}".format(next_action._id, value_max))
    return available_actions.index(next_action)


def read_states_value_from_file(path):
    if os.path.isfile(path):
        with open(path, "rb") as f:
            try:
                return pickle.load(f)
            except Exception:
                print('could not load file {}'.format(path))
                return {}
    return {}


class Player:

    def __init__(self, name, path, human=False, exp_rate=0.0):
        self.name = name
        self.path = path
        self.score = 0
        self.is_human = human
        self.states = []  # record all positions taken
        self.learning_rate = 1 if human else 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 1 if human else 0.80
        self.states_value = read_states_value_from_file(self.path)  # state -> value

    def reset(self):
        self.score = 0
        self.states = []

    def makeAction(self, board: Board):
        if self.is_human:
            action = None
            while action is None:
                while True:
                    try:
                        a = input("Next move: ")
                        if a == 'auto':
                            self.is_human = False
                            return self.makeAction(board)
                        else:
                            a = int(a)
                        break
                    except ValueError:
                        print("Enter a number: ")
                ids = [segment._id for segment in board.available_segments]
                actions = [index for index, _id in enumerate(ids) if _id == a]
                if len(actions) == 1:
                    action = actions[0]
                else:
                    print("Invalid move")
            return action
        action = makeAction(self, board)
        return action

    def updateStates(self, board_hash):
        self.states.append(board_hash)

    def feedReward(self, reward: int):
        decay_gamma = self.decay_gamma
        for state in reversed(self.states):
            if self.states_value.get(state) is None:
                self.states_value[state] = 0.5
            if Settings.VERBOSE_PLAYER:
                print("player {} state value: ".format(self.name), self.states_value[state])
            self.states_value[state] += (self.learning_rate * decay_gamma * (reward - max(self.states_value[state], 0)))
            decay_gamma *= self.decay_gamma
            if Settings.VERBOSE_PLAYER:
                print("player {} new state value: ".format(self.name), self.states_value[state])

    def normalize_state_values(self):
        values = self.states_value.values()
        min_value = min(values)
        max_value = max(values)
        new_values = [(value - min_value) / (max_value - min_value) for value in values]
        for index, key in enumerate(self.states_value.keys()):
            self.states_value[key] = new_values[index]

    def save_states_value(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.states_value, f)
