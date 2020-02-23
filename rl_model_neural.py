from sklearn.neural_network import MLPRegressor
from simple_game import Board, Player
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class RLModel:
    def __init__(self):
        self.reward = 0
        self.learning_rate = 0.0005
        self.board = Board(5)
        self.player = self.board.get_player()
        self.model = self.network()
        self.random_move_predict = .8
        self.state_list = []
        self.reward_list = []
        self.training_list = []

    def network(self, weights=None):
        model = MLPRegressor(hidden_layer_sizes=(10, 10, 10), max_iter=50000)
        return model

    def board_state(self):
        return np.array(self.board.get_state()).reshape((self.board.get_state_size()))

    def make_move(self):
        if random.random() > self.random_move_predict:
            var = random.randint(-1 * self.board.get_width() + 1, self.board.get_width() - 1)
            print("Out:", var)
            return var
        else:
            print("Out:", self.model.predict(self.board_state())[0])
            return int(board.get_width() * (self.model.predict(self.board_state())[0]))

    def addToTrainingList(self):
        dictionary = {}
        numList = [x for x in range(self.board.get_state_size())]
        keyList = ["S" + str(x) for x in numList]
        for i in range(len(keyList)):
            dictionary[keyList[i]] = self.board.get_state()[i]
        dictionary["R"] = self.board.get_reward()
        self.training_list.append(dictionary)
        print(self.training_list)

    def train(self):
        self.addToTrainingList()
        df = pd.DataFrame(self.training_list)
        X = df.iloc[:, :self.board.get_state_size()].values
        y = df["R"].values
        self.model.fit(X, y)

    def get_board(self):
        return self.board

    def get_player(self):
        return self.player

    def new_board(self):
        self.board = Board(5)
        self.player = self.board.get_player()


def plot_seaborn(array_counter, array_score):
    sns.set()
    ax = sns.regplot(np.array([array_counter])[0], np.array([array_score])[0], color="b", x_jitter=.1, line_kws={'color': 'green'})
    ax.set(xlabel='games', ylabel='score')
    plt.show()


if __name__ == "__main__":
    agent = RLModel()
    final_score = []
    for i in range(1000):
        agent.new_board()
        board = agent.get_board()
        player = agent.get_player()
        board.update_current_state()
        agent.train()
        while board.check_survive():
            # board.print_board()
            move = agent.make_move()
            # print("Move: %s" % move)
            player.move(move)
            board.next_row()
            board.update_score()
            board.update_current_state()
            agent.train()
            # print("Reward: %s" % board.get_reward())
            # print("State: %s" % board.get_state())

        print("You Died! \t Final Score: %s" % board.get_score())
        final_score.append(board.get_score())

    print(final_score)
    plot_seaborn([x for x in range(len(final_score))], final_score)
