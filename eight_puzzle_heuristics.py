from eight_puzzle import EightPuzzleBoard
from vec2 import Vec2


def cumulative_distance(current: 'EightPuzzleBoard', goal: 'EightPuzzleBoard'):
    """
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
            # find `val's` goal position
            goal_pos = goal.get_pos_of(val)
            if goal_pos is None:
                # ignore silently if `val` wasnt found...
                continue
            else:
                dist = goal_pos - Vec2(row_i, col_i)
                h += abs(dist.x) + abs(dist.y)
    return h


def count_correct_positions(current: 'EightPuzzleBoard', goal: 'EightPuzzleBoard'):
    counter = 0
    for row1, row2 in zip(current.state, goal.state):
        for val1, val2 in zip(row1, row2):
            counter += 1 if val1 == val2 else 0
    return counter
