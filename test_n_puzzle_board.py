import unittest

from eight_puzzle import EightPuzzleBoard as EPB
from eight_puzzle import MoveDirection as mv


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
