import random


class Board:

    def __init__(self, width):
        self.board_width = width
        self.board_height = 5
        self.curr_board = [[0 for x in range(self.board_width)] for y in range(self.board_height)]
        self.top_row = self.curr_board[0]
        self.player = Player(board_width=self.board_width)
        self.score = 0

    def print_board(self):
        self.curr_board[0][player.get_current_pos()] = "X"
        print("\n\nSCORE: %s" % board.get_score())
        for row in self.curr_board:
            for val in row:
                print(val, end=" ")
            print()
        print("\n")

    def next_row(self):
        del self.curr_board[0]
        self.add_row()

    def add_row(self):
        next_row = [0 for x in range(self.board_width)]
        next_row[random.randint(0, self.board_width-1)] = 1
        self.curr_board.append(next_row)

    def check_survive(self):
        return self.curr_board[0][self.player.get_current_pos()] == 0

    def update_score(self):
        if self.check_survive():
            if self.player.last_move == 0:
                self.score += 1
            else:
                self.score += float(1) / (abs(self.player.last_move)+1)

    def get_score(self):
        return self.score

    def get_player(self):
        return self.player


class Player:

    def __init__(self, board_width):
        self.board_width = board_width
        self.initial_pos = int(board_width / 2)
        self.curr_pos = self.initial_pos
        self.last_move = 0

    def move(self, direction):
        self.last_move = direction
        self.curr_pos = self.curr_pos + direction;
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

    print("You Died! \t Final Score: %s" % board.get_score())

