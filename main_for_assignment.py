"""
This is an example, that mainly utilizes the code in `eight_puzzle` for defining
and solving a predefined puzzle, based on the assignment, this code was originally
written for.
"""

from eight_puzzle import EightPuzzleBoard, EightPuzzle
import eight_puzzle_heuristics as ep_heurs
from search_strategy import BreadthFirstSearch, DepthFirstSearch, AStarSearch


def assignment_example_solution():
    init_state = EightPuzzleBoard([[2, 8, 3], [1, 6, 4], [7, None, 5]])
    goal_state = EightPuzzleBoard([[1, 2, 3], [8, None, 4], [7, 6, 5]])
    # ===================== Breadth First=======================================
    print("~~~ Breadth First ~~~")
    puzzle = EightPuzzle(init_state, goal_state, BreadthFirstSearch())
    print(puzzle)

    print("--- Exhaustive search ---")
    print(puzzle.solve())
    # >>> Iterations to finish: 102
    # >>> [up, up, left, down, right]

    # Returns first found solution
    print("--- Lazy search ---")
    print(puzzle.solve(False))
    # >>> Iterations to finish: 37
    # >>> [up, up, left, down, right]

    # ===================== Depth First ========================================
    print("\n~~~ Depth First ~~~")
    print("(skipping, see source code log)")
    # puzzle = EightPuzzle(init_state, goal_state, DepthFirstSearch())
    # print(puzzle)
    # print("--- Exhaustive search ---")
    # print(puzzle.solve())

    # +++++++++++
    #   -> best found solution after ~6min cpu-time @~4.8GB RAM: 37139 moves
    #   -> no other solution after >30min cpu-time @>5GB RAM
    # ++++++++++

    # ===================== A*-Search ==========================================
    print("\n~~~ A* - Heuristic 1: 'cumulative_distance' ~~~")
    puzzle = EightPuzzle(init_state,
                         goal_state,
                         AStarSearch(goal_state, ep_heurs.cumulative_distance))
    print(puzzle)

    print("--- Exhaustive search ---")
    print(puzzle.solve())
    # >>> Expansions to finish: 102
    # >>> [up, up, left, down, right]

    print("--- Lazy search ---")
    print(puzzle.solve(False))
    # >>> Expansions to finish: 6
    # >>> [up, up, left, down, right]

    print("\n~~~ A* - Heuristic 2: 'count_correct_positions' ~~~")
    puzzle = EightPuzzle(init_state,
                         goal_state,
                         AStarSearch(goal_state, ep_heurs.count_correct_positions))
    print(puzzle)

    print("--- Exhaustive search ---")
    print(puzzle.solve())
    # >>> Expansions to finish: 2665
    # >>> [up, up, left, down, right]

    print("--- Lazy search ---")
    print(puzzle.solve(False))
    # >>> Expansions to finish: 1724
    # >>> [up, up, left, down, right]


def main():
    assignment_example_solution()

    # ==========================================================================

    # An UNSOLVABLE configuration combination
    init_state = EightPuzzleBoard([[4, 7, 8], [5, None, 3], [6, 1, 2]])
    goal_state = EightPuzzleBoard([[1, 2, 3], [8, None, 4], [7, 6, 5]])

    # ===================== Breadth First=======================================
    print("\n~~~ A* - Heuristic 1: 'cumulative_distance' ~~~")
    puzzle = EightPuzzle(init_state,
                         goal_state,
                         AStarSearch(goal_state, ep_heurs.cumulative_distance))
    print(puzzle)

    print("--- Exhaustive search ---")
    print(puzzle.solve())
    # >>> None

    print("--- Lazy search ---")
    print(puzzle.solve(False))
    # >>> None


if __name__ == "__main__":
    main()
