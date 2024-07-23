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


def cumulative_distance_with_linear_conflicts(current: NPuzzleBoard, goal: NPuzzleBoard):
    """
    Aka. 'Manhattan Distance with Linear Conflicts'.

    Extends the regular cumulative distance approach, taking linear conflicts intoaccount.
    Those occur, if two tiles in the same row or column have their respective goal 
    position in said row or column and one has to pass the other on the way to the goal.
    Each such situation implicates at least 2 additional solution steps, as one of the
    tiles has to "move away", let the other pass and move back again (since we are not
    allowed to simply swap tiles).
    """
    h_manhattan = cumulative_distance(current, goal)

    def count_conflicts(current_r_or_c: list, goal_r_or_c: list):
        """
        1) goal_idxs = "for each val retrieve goal index inside current row/col"
        2) for each idx in goal_idxs:
            - check if __subsequent__ elements cross idx's value's goal path 
                - yes: conflict += 2
                - no: next
        """
        def index_or_none(arr, val):
            try:
                return arr.index(val)
            except ValueError:
                return None

        # contains each corresponding goal index (None if not in current row/col)
        goal_idxs = [index_or_none(goal_r_or_c, v) for v in current_r_or_c]

        conflicts = 0
        for i, g_i in enumerate(goal_idxs):
            if current_r_or_c[i] is None:
                continue
            if g_i is None:
                # tile with goal that's not in current row/col
                continue
            else:
                for j in range(i + 1, len(goal_idxs)): # look to the right for conflicts
                    other_g_i = goal_idxs[j]
                    if (other_g_i is not None and other_g_i < g_i):
                        conflicts += 2
        return conflicts

    def get_column(matrix: list[list], col_i: int) -> list:
        return [row[col_i] for row in matrix]

    rows_len, cols_len = (len(current.state), len(current.state[0]))
    conflicts = 0
    for row_i in range(rows_len):
        conflicts += count_conflicts(current.state[row_i], goal.state[row_i])

    for col_i in range(cols_len):
        conflicts += count_conflicts(
            get_column(current.state, col_i),
            get_column(goal.state, col_i))

    return h_manhattan + conflicts


def count_wrong_positions(current: NPuzzleBoard, goal: NPuzzleBoard):
    """Aka. 'Misplaced Tiles Heuristic'."""
    counter = 0
    for row1, row2 in zip(current.state, goal.state):
        for val1, val2 in zip(row1, row2):
            counter += 1 if val1 != val2 else 0
    return counter
