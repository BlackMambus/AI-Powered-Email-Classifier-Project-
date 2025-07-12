import numpy as np
import random

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [' '] * 9
        self.done = False
        return self.get_state()

    def get_state(self):
        return ''.join(self.board)

    def available_actions(self):
        return [i for i, x in enumerate(self.board) if x == ' ']

    def make_move(self, position, player):
        if self.board[position] == ' ':
            self.board[position] = player
            return True
        return False

    def check_winner(self):
        wins = [(0,1,2), (3,4,5), (6,7,8),
                (0,3,6), (1,4,7), (2,5,8),
                (0,4,8), (2,4,6)]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                self.done = True
                return self.board[a]
        if ' ' not in self.board:
            self.done = True
            return 'Draw'
        return None
class QLearningBot:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, actions):
        if random.random() < self.epsilon:
            return random.choice(actions)
        qs = [self.get_q(state, a) for a in actions]
        max_q = max(qs)
        return random.choice([a for a, q in zip(actions, qs) if q == max_q])

    def learn(self, state, action, reward, next_state, next_actions):
        old_q = self.get_q(state, action)
        future_q = max([self.get_q(next_state, a) for a in next_actions], default=0)
        self.q_table[(state, action)] = old_q + self.alpha * (reward + self.gamma * future_q - old_q)
def train(bot, episodes=10000):
    for _ in range(episodes):
        game = TicTacToe()
        state = game.get_state()
        while not game.done:
            actions = game.available_actions()
            action = bot.choose_action(state, actions)
            game.make_move(action, 'X')
            winner = game.check_winner()
            next_state = game.get_state()
            next_actions = game.available_actions()

            if winner == 'X':
                reward = 1
            elif winner == 'Draw':
                reward = 0.5
            elif winner:
                reward = -1
            else:
                reward = 0

            bot.learn(state, action, reward, next_state, next_actions)
            state = next_state
def play_against_bot(bot):
    game = TicTacToe()
    while not game.done:
        print('Board:', game.board)
        if game.board.count('X') <= game.board.count('O'):
            action = bot.choose_action(game.get_state(), game.available_actions())
            game.make_move(action, 'X')
        else:
            move = int(input("Your move (0-8): "))
            if not game.make_move(move, 'O'):
                print("Invalid move.")
                continue
        winner = game.check_winner()
        if winner:
            print('Final Board:', game.board)
            print('Winner:', winner)
            break


