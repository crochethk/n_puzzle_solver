import unittest

from n_puzzle_solver import NPuzzleSolver as Solver
from n_puzzle import MoveDirection as mv, NPuzzleBoard as Board, NPuzzleGame as Game
from n_puzzle_heuristics import *
from search_strategy import *


def run_solve_test(tester: unittest.TestCase, start_board, goal_board, expected_solution):
    puzzle = Game(start_board, goal_board)
    solver = Solver(puzzle, AStarSearch(goal_board, cumulative_distance))
    steps = solver.solve(exhaustive_search=False)
    tester.assertEqual(steps, expected_solution)


class TestNPuzzleSolver(unittest.TestCase):
    def test_solvable_8pg_1(self):
        start = Board([[2, 8, 3], [1, 6, 4], [7, None, 5]])
        goal = Board([[1, 2, 3], [8, None, 4], [7, 6, 5]])
        steps_expected = [mv.UP, mv.UP, mv.LEFT, mv.DOWN, mv.RIGHT]
        run_solve_test(self, start, goal, steps_expected)

    def test_solvable_15pg_1(self):
        start = Board([[1, 2, 3, 4], [5, None, 6, 8], [9, 10, 7, 12], [13, 14, 11, 15]])
        goal = Board([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, None]])
        steps_expected = [mv.RIGHT, mv.DOWN, mv.DOWN, mv.RIGHT]
        run_solve_test(self, start, goal, steps_expected)

    def test_unsolvable_1(self):
        npb8_start = Board([[2, 1, 7], [5, 8, 3], [4, 6, None]])
        npb8_goal = Board([[1, 2, 3], [8, None, 4], [7, 6, 5]])
        steps_expected = None
        run_solve_test(self, npb8_start, npb8_goal, steps_expected)

        npb15_start = Board([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 15, 14, None]])
        npb15_goal = Board([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, None]])
        steps_expected = None
        run_solve_test(self, npb15_start, npb15_goal, steps_expected)


if __name__ == '__main__':
    unittest.main()
