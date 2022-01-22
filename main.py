import numpy as np


class Board:

    def __init__(self, board_state):
        self.board_state = board_state
        self.board_shape = np.array(board_state.shape)
        self.empty_tile_position = np.squeeze(np.argwhere(np.isnan(board_state))) + 1

    def show_available_moves(self):
        available_moves = list()

        if self.empty_tile_position[0] < self.board_shape[0]:
            available_moves.append("up")

        if self.empty_tile_position[0] > 0:
            available_moves.append("down")

        if self.empty_tile_position[1] < self.board_shape[1]:
            available_moves.append("left")

        if self.empty_tile_position[1] > 0:
            available_moves.append("right")

        print(available_moves)


if __name__ == '__main__':
    board = Board(np.array([[1, 2, 3], [4, 5, 6], [7, 8, np.nan]]))
    board.show_available_moves()
