from board import Board

from player import Player
from settings import Settings

player_1 = Player(1, 'first_player_policy')
player_2 = Player(2, 'second_player_policy', Settings.HUMAN_PLAYER)


def train():
    turn = False
    board = Board(Settings.BOARD_DIMENSION, Settings.BOARD_DIMENSION)
    player_1.reset()
    player_2.reset()
    while not board.isComplete():
        if Settings.VERBOSE:
            print("P{0} Plays".format(1 if not turn else 2))
        player = player_2 if turn else player_1
        action = player.makeAction(board)
        board.completeSegment(action)
        player.updateStates(board.getHash(player.score))
        reward = board.getReward()
        if reward > 0:
            if turn:
                player_2.score += reward
            else:
                player_1.score += reward
        for j in range(reward):
            if turn:
                player_2.feedReward(1)
                player_1.feedReward(-1)
            else:
                player_1.feedReward(1)
                player_2.feedReward(-1)

        if Settings.VERBOSE:
            board.printBoard()
            print("P1: {0} - P2: {1}\n".format(player_1.score, player_2.score))
        if reward == 0:
            turn = not turn


def save_state_periodically():
    player_1.save_states_value()
    player_2.save_states_value()
    print(len(player_1.states_value))
    print(len(player_2.states_value))


if Settings.SMART_TRAINING:
    do_train = True
    i = 0
    last_batch_len = 0
    while do_train:
        train()
        i += 1
        if (i + 1) % Settings.BATCH_SIZE == 0:
            print("{0} games simulated, saving state".format(i + 1))
            save_state_periodically()
            if last_batch_len == len(player_1.states_value) + len(player_2.states_value):
                do_train = False
            last_batch_len = len(player_1.states_value) + len(player_2.states_value)

else:
    for i in range(Settings.TRAINING_CYCLES):
        train()
        if (i + 1) % Settings.BATCH_SIZE == 0 or Settings.TRAINING_CYCLES <= 10:
            print("{0} games simulated, saving state".format(i + 1))
            save_state_periodically()
