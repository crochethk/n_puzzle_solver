from n_puzzle import NPuzzleBoard
from vec2 import Vec2


def cumulative_distance(current: NPuzzleBoard, goal: NPuzzleBoard):
    """
    Aka. 'Manhattan Distance Heuristic'.

    Sums step each puzzle piece would need to perform to reach its goal destination,
    assuming an empty board.
    # Example:
    Given a state, which differs from the goal state, in a way, that only two
    adjacent pieces need to be swapped. Then this function returns `2`, since both
    pieces would have to perform one step.
    """
    h = 0
    rows_len, cols_len = (len(current.state), len(current.state[0]))
    for row_i in range(rows_len):
        for col_i in range(cols_len):
            val = current.state[row_i][col_i]
            if val is None:
                continue
            # find `val's` goal position
            goal_pos = goal.get_pos_of(val)
            if goal_pos is None:
                # ignore silently if `val` wasnt found...
                continue
            else:
                h += current.step_distance(Vec2(row_i, col_i), goal_pos)
    return h


def count_wrong_positions(current: NPuzzleBoard, goal: NPuzzleBoard):
    """Aka. 'Misplaced Tiles Heuristic'."""
    counter = 0
    for row1, row2 in zip(current.state, goal.state):
        for val1, val2 in zip(row1, row2):
            counter += 1 if val1 != val2 else 0
    return counter
