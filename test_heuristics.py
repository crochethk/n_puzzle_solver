import unittest

import n_puzzle_heuristics as epheur
from n_puzzle import NPuzzleBoard as Board


class TestHeuristics(unittest.TestCase):
    def test_count_wrong_heur_1(self):
        curr = Board([[2, 8, 3], [1, 6, 4], [7, None, 5]])
        goal = Board([[1, 2, 3], [8, None, 4], [7, 6, 5]])
        self.assertEqual(epheur.count_wrong_positions(
            curr, goal), 5)

    def test_count_wrong_heur_2(self):
        curr = Board([[2, 8, 3], [1, None, 4], [7, 6, 5]])
        goal = Board([[1, 2, 3], [8, None, 4], [7, 6, 5]])
        self.assertEqual(epheur.count_wrong_positions(
            curr, goal), 3)

    def test_cumulative_distance_heur_1(self):
        curr = Board([[2, 8, 3], [1, 6, 4], [7, None, 5]])
        goal = Board([[2, 8, 3], [1, 6, 4], [None, 7, 5]])
        self.assertEqual(epheur.cumulative_distance(curr, goal), 1)

    def test_cumulative_distance_heur_2(self):
        curr = Board([[8, 2, 3], [4, 5, 6], [7, None, 1]])
        goal = Board([[1, 2, 3], [4, 5, 6], [7, 8, None]])
        self.assertEqual(epheur.cumulative_distance(curr, goal), 7)
        curr, goal = (goal, curr)
        self.assertEqual(epheur.cumulative_distance(curr, goal), 7)


if __name__ == '__main__':
    unittest.main()
