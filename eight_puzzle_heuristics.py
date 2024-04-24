
def cumulative_distance(current: 'EightPuzzleBoard', goal: 'EightPuzzleBoard'):  # type: ignore
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
    for row_idx in range(rows_len):
        for col_idx in range(cols_len):
            val = current.state[row_idx][col_idx]
            # find `val's` goal position
            goal_pos = goal.get_pos_of(val)
            if goal_pos is None:
                # ignore silently if `val` wasnt found...
                continue
            else:
                drow = goal_pos[0] - row_idx
                dcol = goal_pos[1] - col_idx
                h += abs(drow) + abs(dcol)
    return h


def count_correct_positions(current: 'EightPuzzleBoard', goal: 'EightPuzzleBoard'):  # type: ignore
    counter = 0
    for row1, row2 in zip(current.state, goal.state):
        for val1, val2 in zip(row1, row2):
            counter += 1 if val1 == val2 else 0
    return counter
