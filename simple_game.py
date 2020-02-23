import random


class Board:

    def __init__(self, width):
        self.board_width = width
        self.board_height = 5
        self.curr_board = [[0 for x in range(self.board_width)] for y in range(self.board_height)]
        self.top_row = self.curr_board[0]
        self.player = Player(board_width=self.board_width)
        self.score = 0
        self.alive = True
        self.curr_state = []
        self.last_state = []
        self.reward = 0

    def print_board(self):
        self.curr_board[0][self.player.get_current_pos()] = "X"
        print("SCORE: %s\n" % self.get_score())
        for row in self.curr_board:
            for val in row:
                print(val, end=" ")
            print()
        print("\n")

    def next_row(self):
        del self.curr_board[0]
        self.add_row()
        self.check_survive()

    def add_row(self):
        next_row = [0 for x in range(self.board_width)]
        next_row[random.randint(0, self.board_width-1)] = 1
        self.curr_board.append(next_row)

    def check_survive(self):
        self.alive = self.curr_board[0][self.player.get_current_pos()] == 0
        return self.alive

    def update_score(self):
        if self.check_survive():
            if self.player.last_move == 0:
                self.reward = 1
                self.score += 1
            else:
                self.reward = float(1) / (abs(self.player.last_move)+1)
                self.score += float(1) / (abs(self.player.last_move)+1)
        else:
            self.reward = -1

    def update_current_state(self):
        self.last_state = self.curr_state
        # Alive/Dead, Current Position, Matrix Values
        state = [self.player.curr_pos]
        for row in self.curr_board:
            for val in row:
                state.append(val)
        self.curr_state = state

    def get_score(self):
        return self.score

    def get_player(self):
        return self.player

    def get_reward(self):
        return self.reward

    def get_width(self):
        return self.board_width

    def get_state(self):
        return self.curr_state

    def get_state_size(self):
        return 1 + self.board_width*self.board_height


class Player:

    def __init__(self, board_width):
        self.board_width = board_width
        self.initial_pos = int(board_width / 2)
        self.curr_pos = self.initial_pos
        self.last_move = 0

    def move(self, direction):
        self.last_move = direction
        self.curr_pos = self.curr_pos + direction
        if self.curr_pos < 0:
            self.curr_pos = 0
        elif self.curr_pos >= self.board_width:
            self.curr_pos = self.board_width - 1

    def get_current_pos(self):
        return self.curr_pos


if __name__ == "__main__":
    board = Board(width=5)
    player = board.get_player()
    while board.check_survive():
        board.print_board()
        player.move(int(input("DIR: ")))
        board.next_row()
        board.update_score()
        board.update_current_state()


    print("You Died! \t Final Score: %s" % board.get_score())

