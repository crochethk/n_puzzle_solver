"""
This is an example, that mainly utilizes the code in `n_puzzle` and `n_puzzle_solver`
for defining and solving a predefined puzzle, based on the assignment, this code was 
originally written for.
"""

import n_puzzle_heuristics as heuristics
from n_puzzle import NPuzzleBoard as EightPuzzleBoard, NPuzzleGame as EightPuzzle
from search_strategy import BreadthFirstSearch, DepthFirstSearch, AStarSearch
from n_puzzle_solver import NPuzzleSolver as Solver


def assignment_example_solution():
    init_state = EightPuzzleBoard([[2, 8, 3], [1, 6, 4], [7, None, 5]])
    goal_state = EightPuzzleBoard([[1, 2, 3], [8, None, 4], [7, 6, 5]])
    # ===================== Breadth First=======================================
    print("~~~ Breadth First ~~~")
    puzzle = EightPuzzle(init_state, goal_state)
    solver = Solver(puzzle, BreadthFirstSearch())

    print("--- Exhaustive search ---")
    print(solver.solve(True))
    # >>> Iterations to finish: 102
    # >>> [up, up, left, down, right]

    # Returns first found solution
    print("--- Lazy search ---")
    print(solver.solve(False))

    # >>> Iterations to finish: 37
    # >>> [up, up, left, down, right]

    # ===================== Depth First ========================================
    print("\n~~~ Depth First ~~~")
    print("(skipping these, see source code log)")
    # puzzle = EightPuzzle(init_state, goal_state)
    # solver = Solver(puzzle, DepthFirstSearch())
    # print("--- Exhaustive search ---")
    # print(solver.solve(True))

    # +++++++++++
    #   -> best found solution after ~6min cpu-time @~4.8GB RAM: 37139 moves
    #   -> no other solution after >30min cpu-time @>5GB RAM
    # ++++++++++

    # ===================== A*-Search ==========================================
    print("\n~~~ A* - Heuristic 1: 'cumulative_distance' ~~~")
    puzzle = EightPuzzle(init_state, goal_state)
    solver = Solver(puzzle, AStarSearch(goal_state, heuristics.cumulative_distance))

    print("--- Exhaustive search ---")
    print(solver.solve(True))
    # >>> Expansions to finish: 100
    # >>> [up, up, left, down, right]

    print("--- Lazy search ---")
    print(solver.solve(False))
    # >>> Expansions to finish: 6
    # >>> [up, up, left, down, right]

    print("\n~~~ A* - Heuristic 2: 'count_wrong_positions' ~~~")
    puzzle = EightPuzzle(init_state, goal_state)
    solver = Solver(puzzle, AStarSearch(goal_state, heuristics.count_wrong_positions))

    print("--- Exhaustive search ---")
    print(solver.solve(True))
    # >>> Expansions to finish: 102
    # >>> [up, up, left, down, right]

    print("--- Lazy search ---")
    print(solver.solve(False))
    # >>> Expansions to finish: 6
    # >>> [up, up, left, down, right]


def main():
    assignment_example_solution()

    # ==========================================================================

    # An UNSOLVABLE configuration combination
    init_state = EightPuzzleBoard([[4, 7, 8], [5, None, 3], [6, 1, 2]])
    goal_state = EightPuzzleBoard([[1, 2, 3], [8, None, 4], [7, 6, 5]])

    # ===================== Breadth First=======================================
    print("\n~~~ A* - Heuristic 1: 'cumulative_distance' ~~~")
    puzzle = EightPuzzle(init_state, goal_state)
    solver = Solver(puzzle, AStarSearch(goal_state, heuristics.cumulative_distance))

    print("--- Exhaustive search ---")
    print(solver.solve(True))
    # >>> None

    print("--- Lazy search ---")
    print(solver.solve(False))
    # >>> None


if __name__ == "__main__":
    main()
