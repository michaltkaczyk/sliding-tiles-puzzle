import numpy as np


class Board:

    def __init__(self, board_state):
        self.board_state = board_state
        self.board_shape = np.array(board_state.shape)
        self.empty_tile_position = np.squeeze(np.argwhere(np.isnan(board_state)))
        self.ideal_board_state = self.create_ideal_board()
        self.distance = self.calculate_distance()

    def create_ideal_board(self):
        x = np.arange(self.board_shape[0] * self.board_shape[1] - 1) + 1
        x = np.append(x, np.nan)
        x = np.reshape(x, self.board_shape)
        return x

    def calculate_distance(self):
        distance_matrix = np.zeros((self.board_shape[0], self.board_shape[1]))

        for row in range(self.board_shape[0]):
            for column in range(self.board_shape[1]):
                item = self.ideal_board_state[row, column]

                if not np.isnan(item):
                    item_current_row = np.where(self.board_state == item)[0][0]
                    item_current_column = np.where(self.board_state == item)[1][0]

                    row_distance = abs(item_current_row - row)
                    column_distance = abs(item_current_column - column)

                    distance_matrix[row, column] = row_distance + column_distance

        return np.sum(distance_matrix)

    def show_available_moves(self):
        available_moves = list()

        if self.empty_tile_position[0] + 1 < self.board_shape[0]:
            available_moves.append("up")

        if self.empty_tile_position[0] > 0:
            available_moves.append("down")

        if self.empty_tile_position[1] + 1 < self.board_shape[1]:
            available_moves.append("left")

        if self.empty_tile_position[1] > 0:
            available_moves.append("right")

        return available_moves

    def move_right(self):
        self.board_state[self.empty_tile_position[0], self.empty_tile_position[1]] =\
            self.board_state[self.empty_tile_position[0], self.empty_tile_position[1] - 1]

        self.board_state[self.empty_tile_position[0], self.empty_tile_position[1] - 1] = np.nan

        self.empty_tile_position = np.squeeze(np.argwhere(np.isnan(self.board_state)))
        self.distance = self.calculate_distance()

    def move_left(self):
        self.board_state[self.empty_tile_position[0], self.empty_tile_position[1]] =\
            self.board_state[self.empty_tile_position[0], self.empty_tile_position[1] + 1]

        self.board_state[self.empty_tile_position[0], self.empty_tile_position[1] + 1] = np.nan

        self.empty_tile_position = np.squeeze(np.argwhere(np.isnan(self.board_state)))
        self.distance = self.calculate_distance()

    def move_up(self):
        self.board_state[self.empty_tile_position[0], self.empty_tile_position[1]] = \
            self.board_state[self.empty_tile_position[0] + 1, self.empty_tile_position[1]]

        self.board_state[self.empty_tile_position[0] + 1, self.empty_tile_position[1]] = np.nan

        self.empty_tile_position = np.squeeze(np.argwhere(np.isnan(self.board_state)))
        self.distance = self.calculate_distance()

    def move_down(self):
        self.board_state[self.empty_tile_position[0], self.empty_tile_position[1]] = \
            self.board_state[self.empty_tile_position[0] - 1, self.empty_tile_position[1]]

        self.board_state[self.empty_tile_position[0] - 1, self.empty_tile_position[1]] = np.nan

        self.empty_tile_position = np.squeeze(np.argwhere(np.isnan(self.board_state)))
        self.distance = self.calculate_distance()


if __name__ == '__main__':
    board = Board(np.array([[4, 2, 3], [8, 5, 6], [7, 1, np.nan]]))

    print(board.show_available_moves())

    print(board.board_state)
    print(board.distance)
    board.move_right()

    print(board.board_state)
    print(board.distance)
    board.move_left()

    print(board.board_state)
    print(board.distance)
    board.move_down()

    print(board.board_state)
    print(board.distance)
    board.move_up()

    print(board.board_state)
    print(board.distance)
