import sys
import torch
import random
import numpy as np
from collections import deque
from game import Game
from model import Linear_QNet, QTrainer
from helper import plot
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter("runs/DQN_Model")
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self, board_size):
        self.board_size = board_size
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft
        self.model = Linear_QNet()
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = []
        board = game.board
        for row in range(board.size[0]):
            for col in range(board.size[1]):
                piece = board.get_piece(row, col)
                if piece.get_clicked():
                    state.append(piece.get_num_around() / 10)
                else:
                    if piece.get_flagged():
                        state.append(0.9)
                    else:
                        state.append(1)

        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random actions tradeoff: exploitation / exploration
        self.epsilon = 5000 - self.n_games
        final_move = None
        if random.randint(0, 5000) < self.epsilon:
            move = random.randint(0, self.board_size * self.board_size - 1)
            final_move = move
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction)
            final_move = int(move)

        return final_move


def train():
    """plot_rewards = []
    plot_mean_rewards = []
    total_reward = 0"""
    agent = Agent(5)
    screen_size = (600, 600)
    game = Game(screen_size)
    writer.add_graph(agent.model, torch.tensor(agent.get_state(game), dtype=torch.float))
    writer.close()
    running_loss = 0.0
    won_games = 0
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        done, step_reward = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, step_reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, step_reward, state_new, done)
        running_loss += agent.trainer.loss.item()

        if done:
            if game.board.get_won():
                won_games +=1
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            agent.model.save()
            writer.add_scalar("won games / tot games", won_games, agent.n_games)
            if agent.n_games % 30 == 0:
                writer.add_scalar("running loss", running_loss / 30, agent.n_games)
                running_loss = 0.0

            if agent.n_games == 5000:
                writer.add_scalar("running loss", running_loss / 30, agent.n_games)
                break

            """plot_rewards.append(reward)
            total_reward += reward
            mean_reward = total_reward / agent.n_games
            plot_mean_rewards.append(mean_reward)
            plot(plot_rewards, plot_mean_rewards)"""



if __name__ == '__main__':
    train()

