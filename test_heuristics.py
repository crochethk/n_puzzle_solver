import unittest

import n_puzzle_heuristics as epheur
from eight_puzzle import EightPuzzleBoard as EPB


class TestHeuristics(unittest.TestCase):
    def test_count_correct_heur_1(self):
        curr = EPB([[2, 8, 3], [1, 6, 4], [7, None, 5]])
        goal = EPB([[1, 2, 3], [8, None, 4], [7, 6, 5]])
        self.assertEqual(epheur.count_correct_positions(
            curr, goal), 4)
        self.assertNotEqual(epheur.count_correct_positions(
            curr, goal), 3)

    def test_count_correct_heur_2(self):
        curr = EPB([[2, 8, 3], [1, None, 4], [7, 6, 5]])
        goal = EPB([[1, 2, 3], [8, None, 4], [7, 6, 5]])
        self.assertEqual(epheur.count_correct_positions(
            curr, goal), 6)
        self.assertNotEqual(epheur.count_correct_positions(
            curr, goal), 4)

    def test_cumulative_distance_heur_1(self):
        curr = EPB([[2, 8, 3], [1, 6, 4], [7, None, 5]])
        goal = EPB([[2, 8, 3], [1, 6, 4], [None, 7, 5]])
        self.assertEqual(epheur.cumulative_distance(curr, goal), 2)
        self.assertNotEqual(epheur.cumulative_distance(curr, goal), 1)

    def test_cumulative_distance_heur_2(self):
        curr = EPB([[8, 2, 3], [4, 5, 6], [7, None, 1]])
        goal = EPB([[1, 2, 3], [4, 5, 6], [7, 8, None]])
        self.assertEqual(epheur.cumulative_distance(curr, goal), 8)
        curr, goal = (goal, curr)
        self.assertEqual(epheur.cumulative_distance(curr, goal), 8)


if __name__ == '__main__':
    unittest.main()
