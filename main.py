import copy
import numpy as np

DIRECTION_VECTORS = {
    "right": (0, -1),
    "left": (0, 1),
    "down": (-1, 0),
    "up": (1, 0),
}

ITERATIONS_LIMIT = 100


def calculate_distance(board_state, final_board_state):
    distance_matrix = np.zeros(np.array(board_state.shape))

    for row in range(board_state.shape[0]):
        for column in range(board_state.shape[1]):
            item = final_board_state[row, column]

            # Position of the empty tile (coded as 0) is not included in the distance calculation

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
        # As opposed to the original problem description, position of the empty tile (coded as 0) for a solved board is
        # not in the middle, but rather in the bottom-right corner. This allows solving any n x m rectangular puzzle,
        # rather than just (2n+1) x (2n+1) ones.

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

        self.board_states_to_see = [self.initial_board_state]  # L
        self.seen_board_states = []                            # L_seen

    def run(self):
        while len(self.board_states_to_see) > 0 and self.success is False and self.iteration < ITERATIONS_LIMIT:
            currently_analyzed_board_state = self.board_states_to_see[0]  # n
            print(currently_analyzed_board_state)

            self.seen_board_states.append(currently_analyzed_board_state)
            self.board_states_to_see.pop(0)

            if calculate_distance(currently_analyzed_board_state, self.final_board_state) == 0:
                print("The problem was successfully solved in", self.iteration, "moves!")

                self.success = True
            else:
                available_moves = show_available_moves(currently_analyzed_board_state)

                for direction in available_moves:
                    if available_moves[direction] is True:
                        new_board_state = move(currently_analyzed_board_state, direction)
                        if not np.any(np.all(new_board_state == self.seen_board_states, axis=(1, 2))):
                            self.board_states_to_see.append(new_board_state)

                analyzed_board_states_distances = []

                for board_state in self.board_states_to_see:
                    analyzed_board_states_distances.append(calculate_distance(board_state, self.final_board_state))

                self.board_states_to_see = [board_state for _, board_state in
                                            sorted(zip(analyzed_board_states_distances, self.board_states_to_see),
                                                   key=lambda pair: pair[0])]
                self.iteration += 1

        if self.success is False:
            if len(self.board_states_to_see) == 0:
                print("There are no more states for the algorithm to check. The problem is unsolvable.")
            elif self.iteration == ITERATIONS_LIMIT:
                print("The algorithm exceeded the available number of iterations.")


if __name__ == '__main__':
    print("\nSolving a solved board:")
    board_b = Board(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]))
    search = Search(board_b)
    search.run()

    print("\nSolving an easy board:")
    board_a = Board(np.array([[1, 2, 3], [4, 0, 6], [7, 5, 8]]))
    search = Search(board_a)
    search.run()

    print("\nSolving an unsolvable board (2 x 2):")
    board_c = Board(np.array([[1, 3], [2, 0]]))
    search = Search(board_c)
    search.run()

    print("\nSolving an unsolvable board (3 x 3):")
    board_d = Board(np.array([[1, 2, 3], [4, 5, 6], [8, 7, 0]]))
    search = Search(board_d)
    search.run()
