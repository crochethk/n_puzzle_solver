import unittest
from eight_puzzle import EightPuzzleBoard as EPB
from eight_puzzle import MoveDirection as mv
import eight_puzzle_heuristics as epheur


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


class TestEPBoard(unittest.TestCase):
    def test_next_states_1(self):
        s_init = [[2, 8, 3], [1, 6, 4], [7, None, 5]]
        history = []
        expect_next_states = [
            ([mv.UP], EPB([[2, 8, 3], [1, None, 4], [7, 6, 5]])),
            ([mv.RIGHT], EPB([[2, 8, 3], [1, 6, 4], [7, 5, None]])),
            ([mv.LEFT], EPB([[2, 8, 3], [1, 6, 4], [None, 7, 5]])),
        ]
        next_states = EPB(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_2(self):
        s_init = [[2, 8, 3], [1, 6, 4], [None, 7, 5]]
        history = [mv.DOWN]
        expect_next_states = [
            ([mv.DOWN, mv.UP], EPB([[2, 8, 3], [None, 6, 4], [1, 7, 5]])),
            ([mv.DOWN, mv.RIGHT], EPB([[2, 8, 3], [1, 6, 4], [7, None, 5]])),
        ]
        next_states = EPB(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_3(self):
        s_init = [[2, 8, 3], [1, None, 4], [7, 6, 5]]
        history = [mv.LEFT]
        expect_next_states = [
            ([mv.LEFT, mv.DOWN], EPB([[2, 8, 3], [1, 6, 4], [7, None, 5]])),
            ([mv.LEFT, mv.UP], EPB([[2, None, 3], [1, 8, 4], [7, 6, 5]])),
            ([mv.LEFT, mv.RIGHT], EPB([[2, 8, 3], [1, 4, None], [7, 6, 5]])),
            ([mv.LEFT, mv.LEFT], EPB([[2, 8, 3], [None, 1, 4], [7, 6, 5]])),
        ]
        next_states = EPB(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_4(self):
        s_init = [[2, 8, 3], [1, 4, None], [7, 6, 5]]
        history = [mv.UP]
        expect_next_states = [
            ([mv.UP, mv.DOWN], EPB([[2, 8, 3], [1, 4, 5], [7, 6, None]])),
            ([mv.UP, mv.UP], EPB([[2, 8, None], [1, 4, 3], [7, 6, 5]])),
            ([mv.UP, mv.LEFT], EPB([[2, 8, 3], [1, None, 4], [7, 6, 5]])),
        ]
        next_states = EPB(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_5(self):
        s_init = [[2, None, 3], [1, 8, 4], [7, 6, 5]]
        history = [mv.RIGHT]
        expect_next_states = [
            ([mv.RIGHT, mv.DOWN], EPB([[2, 8, 3], [1, None, 4], [7, 6, 5]])),
            ([mv.RIGHT, mv.RIGHT], EPB([[2, 3, None], [1, 8, 4], [7, 6, 5]])),
            ([mv.RIGHT, mv.LEFT], EPB([[None, 2, 3], [1, 8, 4], [7, 6, 5]])),
        ]
        next_states = EPB(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)


if __name__ == '__main__':
    unittest.main()
