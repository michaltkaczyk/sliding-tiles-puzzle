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
        print("distance:", self.distance)

        if self.empty_tile_position[0] + 1 < self.board_shape[0]:
            available_moves.append("up")
            self.move("up")
            print("on move up distance would be:", self.distance)
            self.move("down")

        if self.empty_tile_position[0] > 0:
            available_moves.append("down")
            self.move("down")
            print("on move down distance would be:", self.distance)
            self.move("up")

        if self.empty_tile_position[1] + 1 < self.board_shape[1]:
            available_moves.append("left")
            self.move("left")
            print("on move left distance would be:", self.distance)
            self.move("right")

        if self.empty_tile_position[1] > 0:
            available_moves.append("right")
            self.move("right")
            print("on move right distance would be:", self.distance)
            self.move("left")

        return available_moves

    DIRECTION_VECTORS = {
        "right": (0, -1),
        "left": (0, 1),
        "down": (-1, 0),
        "up": (1, 0),
    }

    def move(self, direction):
        if direction in self.DIRECTION_VECTORS:
            old_index = (self.empty_tile_position[0], self.empty_tile_position[1])
            new_index = tuple(sum(x) for x in zip(old_index, self.DIRECTION_VECTORS[direction]))

            self.board_state[old_index] = self.board_state[new_index]
            self.board_state[new_index] = np.nan

            self.empty_tile_position = np.squeeze(np.argwhere(np.isnan(self.board_state)))
            self.distance = self.calculate_distance()
        else:
            raise ValueError("direction not recognized")


if __name__ == '__main__':
    board = Board(np.array([[7, 4, 8], [1, np.nan, 5], [6, 2, 3]]))

    print(board.show_available_moves())

    print(board.board_state)
    print(board.distance)
    board.move("right")

    print(board.board_state)
    print(board.distance)
    board.move("left")

    print(board.board_state)
    print(board.distance)
    board.move("down")

    print(board.board_state)
    print(board.distance)
    board.move("up")

    print(board.board_state)
    print(board.distance)
