import copy
import numpy as np


DIRECTION_VECTORS = {
    "right": (0, -1),
    "left": (0, 1),
    "down": (-1, 0),
    "up": (1, 0),
}


def calculate_distance(board_state, final_board_state):
    distance_matrix = np.zeros(np.array(board_state.shape))

    for row in range(board_state.shape[0]):
        for column in range(board_state.shape[1]):
            item = final_board_state[row, column]

            if not item == 0:
                item_current_row = np.where(board_state == item)[0][0]
                item_current_column = np.where(board_state == item)[1][0]

                row_distance = abs(item_current_row - row)
                column_distance = abs(item_current_column - column)

                distance_matrix[row, column] = row_distance + column_distance

    return np.sum(distance_matrix)


def show_available_moves(board_state):
    empty_tile_position = tuple(np.argwhere(board_state == 0)[0])

    available_moves = {
        "right": False,
        "left": False,
        "down": False,
        "up": False,
    }

    if empty_tile_position[0] + 1 < board_state.shape[0]:
        available_moves["up"] = True

    if empty_tile_position[0] > 0:
        available_moves["down"] = True

    if empty_tile_position[1] + 1 < board_state.shape[1]:
        available_moves["left"] = True

    if empty_tile_position[1] > 0:
        available_moves["right"] = True

    return available_moves


def move(board_state, direction):
    empty_tile_position = tuple(np.argwhere(board_state == 0)[0])

    if direction in DIRECTION_VECTORS:
        old_index = (empty_tile_position[0], empty_tile_position[1])
        new_index = tuple(sum(x) for x in zip(old_index, DIRECTION_VECTORS[direction]))

        new_board_state = copy.deepcopy(board_state)

        new_board_state[old_index] = board_state[new_index]
        new_board_state[new_index] = 0

        return new_board_state
    else:
        raise ValueError("direction not recognized")


class Board:

    def __init__(self, board_state):
        self.board_state = board_state
        self.board_shape = np.array(board_state.shape)
        self.empty_tile_position = tuple(np.argwhere(board_state == 0)[0])
        self.final_board_state = self.create_ideal_board()
        self.distance = calculate_distance(self.board_state, self.final_board_state)

    def create_ideal_board(self):
        x = np.arange(self.board_shape[0] * self.board_shape[1] - 1) + 1
        x = np.append(x, 0)
        x = np.reshape(x, self.board_shape)
        return x


class Search:

    def __init__(self, board):
        self.initial_board_state = board.board_state
        self.final_board_state = board.final_board_state

        self.success = False
        self.iteration = 0

        self.analyzed_board_states = [self.initial_board_state]         # L
        self.seen_board_states = []                                     # L_seen

    def run(self):
        while len(self.analyzed_board_states) > 0 and self.success == False and self.iteration < 100:

            currently_analyzed_board_state = self.analyzed_board_states[0]  # n
            self.analyzed_board_states.pop()

            if calculate_distance(currently_analyzed_board_state, self.final_board_state) == 0:
                print("success!")
                self.success = True
            else:
                print("working on it...")

                available_moves = show_available_moves(currently_analyzed_board_state)

                for direction in available_moves:
                    if available_moves[direction] is True:
                        new_board_state = move(currently_analyzed_board_state, direction)
                        if new_board_state not in self.seen_board_states:
                            self.analyzed_board_states.append(new_board_state)

                analyzed_board_states_distances = []

                for board_state in self.analyzed_board_states:
                    analyzed_board_states_distances.append(calculate_distance(board_state, self.final_board_state))

                self.analyzed_board_states =\
                    [self.analyzed_board_states[i] for i in np.argsort(analyzed_board_states_distances)]

                self.iteration += 1


if __name__ == '__main__':
    print("Solving board A:")
    board_a = Board(np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]]))
    search = Search(board_a)
    search.run()

    print("\nSolving board B:")
    board_b = Board(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]))
    search = Search(board_b)
    search.run()
