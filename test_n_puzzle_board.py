import unittest

from n_puzzle import NPuzzleBoard as Board
from n_puzzle import MoveDirection as mv


class Test8PuzzleBoard(unittest.TestCase):
    def test_next_states_1(self):
        s_init = [[2, 8, 3], [1, 6, 4], [7, None, 5]]
        history = []
        expect_next_states = [
            ([mv.UP], Board([[2, 8, 3], [1, None, 4], [7, 6, 5]])),
            ([mv.RIGHT], Board([[2, 8, 3], [1, 6, 4], [7, 5, None]])),
            ([mv.LEFT], Board([[2, 8, 3], [1, 6, 4], [None, 7, 5]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_2(self):
        s_init = [[2, 8, 3], [1, 6, 4], [None, 7, 5]]
        history = [mv.DOWN]
        expect_next_states = [
            ([mv.DOWN, mv.UP], Board([[2, 8, 3], [None, 6, 4], [1, 7, 5]])),
            ([mv.DOWN, mv.RIGHT], Board([[2, 8, 3], [1, 6, 4], [7, None, 5]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_3(self):
        s_init = [[2, 8, 3], [1, None, 4], [7, 6, 5]]
        history = [mv.LEFT]
        expect_next_states = [
            ([mv.LEFT, mv.DOWN], Board([[2, 8, 3], [1, 6, 4], [7, None, 5]])),
            ([mv.LEFT, mv.UP], Board([[2, None, 3], [1, 8, 4], [7, 6, 5]])),
            ([mv.LEFT, mv.RIGHT], Board([[2, 8, 3], [1, 4, None], [7, 6, 5]])),
            ([mv.LEFT, mv.LEFT], Board([[2, 8, 3], [None, 1, 4], [7, 6, 5]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_4(self):
        s_init = [[2, 8, 3], [1, 4, None], [7, 6, 5]]
        history = [mv.UP]
        expect_next_states = [
            ([mv.UP, mv.DOWN], Board([[2, 8, 3], [1, 4, 5], [7, 6, None]])),
            ([mv.UP, mv.UP], Board([[2, 8, None], [1, 4, 3], [7, 6, 5]])),
            ([mv.UP, mv.LEFT], Board([[2, 8, 3], [1, None, 4], [7, 6, 5]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_5(self):
        s_init = [[2, None, 3], [1, 8, 4], [7, 6, 5]]
        history = [mv.RIGHT]
        expect_next_states = [
            ([mv.RIGHT, mv.DOWN], Board([[2, 8, 3], [1, None, 4], [7, 6, 5]])),
            ([mv.RIGHT, mv.RIGHT], Board([[2, 3, None], [1, 8, 4], [7, 6, 5]])),
            ([mv.RIGHT, mv.LEFT], Board([[None, 2, 3], [1, 8, 4], [7, 6, 5]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)


class Test15PuzzleBoard(unittest.TestCase):
    def test_next_states_1(self): # "inner row"
        s_init = [[2, 8, 3, 9], [1, 6, 4, 10], [7, None, 5, 11], [12, 13, 14, 15]]
        history = []
        expect_next_states = [
            ([mv.DOWN], Board([[2, 8, 3, 9], [1, 6, 4, 10], [7, 13, 5, 11], [12, None, 14, 15]])),
            ([mv.UP], Board([[2, 8, 3, 9], [1, None, 4, 10], [7, 6, 5, 11], [12, 13, 14, 15]])),
            ([mv.RIGHT], Board([[2, 8, 3, 9], [1, 6, 4, 10], [7, 5, None, 11], [12, 13, 14, 15]])),
            ([mv.LEFT], Board([[2, 8, 3, 9], [1, 6, 4, 10], [None, 7, 5, 11], [12, 13, 14, 15]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_2(self): # "inner row"
        s_init = [[2, 8, 3, 9], [1, 6, 4, 10], [None, 7, 5, 11], [12, 13, 14, 15]]
        history = [mv.DOWN]
        expect_next_states = [
            ([mv.DOWN, mv.DOWN], Board([[2, 8, 3, 9], [1, 6, 4, 10], [12, 7, 5, 11], [None, 13, 14, 15]])),
            ([mv.DOWN, mv.UP], Board([[2, 8, 3, 9], [None, 6, 4, 10], [1, 7, 5, 11], [12, 13, 14, 15]])),
            ([mv.DOWN, mv.RIGHT], Board([[2, 8, 3, 9], [1, 6, 4, 10], [7, None, 5, 11], [12, 13, 14, 15]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_3(self): # "inner row"
        s_init = [[2, 8, 3, 9], [1, 4, 10, None], [7, 6, 5, 11], [12, 13, 14, 15]]
        history = [mv.UP]
        expect_next_states = [
            ([mv.UP, mv.DOWN], Board([[2, 8, 3, 9], [1, 4, 10, 11], [7, 6, 5, None], [12, 13, 14, 15]])),
            ([mv.UP, mv.UP], Board([[2, 8, 3, None], [1, 4, 10, 9], [7, 6, 5, 11], [12, 13, 14, 15]])),
            ([mv.UP, mv.LEFT], Board([[2, 8, 3, 9], [1, 4, None, 10], [7, 6, 5, 11], [12, 13, 14, 15]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_4(self): # "bottom row"
        s_init = [[2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15], [7, None, 5, 11]]
        history = [mv.LEFT]
        expect_next_states = [
            ([mv.LEFT, mv.UP], Board([[2, 8, 3, 9], [1, 6, 4, 10], [12, None, 14, 15], [7, 13, 5, 11]])),
            ([mv.LEFT, mv.RIGHT], Board([[2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15], [7, 5, None, 11]])),
            ([mv.LEFT, mv.LEFT], Board([[2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15], [None, 7, 5, 11]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_5(self): # "bottom row"
        s_init = [[2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15], [None, 7, 5, 11]]
        history = [mv.RIGHT]
        expect_next_states = [
            ([mv.RIGHT, mv.UP], Board([[2, 8, 3, 9], [1, 6, 4, 10], [None, 13, 14, 15], [12, 7, 5, 11]])),
            ([mv.RIGHT, mv.RIGHT], Board([[2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15], [7, None, 5, 11]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_6(self): # "bottom row"
        s_init = [[2, 8, 3, 9], [7, 6, 5, 11], [12, 13, 14, 15], [1, 4, 10, None]]
        history = []
        expect_next_states = [
            ([mv.UP], Board([[2, 8, 3, 9], [7, 6, 5, 11], [12, 13, 14, None], [1, 4, 10, 15]])),
            ([mv.LEFT], Board([[2, 8, 3, 9], [7, 6, 5, 11], [12, 13, 14, 15], [1, 4, None, 10]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_7(self): # "top row"
        s_init = [[7, None, 5, 11], [2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15],]
        history = []
        expect_next_states = [
            ([mv.DOWN], Board([[7, 8, 5, 11], [2, None, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15]])),
            ([mv.RIGHT], Board([[7, 5, None, 11], [2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15]])),
            ([mv.LEFT], Board([[None, 7, 5, 11], [2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15]])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_8(self): # "top row"
        s_init = [[None, 7, 5, 11], [2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15],]
        history = []
        expect_next_states = [
            ([mv.DOWN], Board([[2, 7, 5, 11], [None, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15],])),
            ([mv.RIGHT], Board([[7, None, 5, 11], [2, 8, 3, 9], [1, 6, 4, 10], [12, 13, 14, 15],])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)

    def test_next_states_9(self): # "top row"
        s_init = [[1, 4, 10, None], [2, 8, 3, 9], [7, 6, 5, 11], [12, 13, 14, 15],]
        history = []
        expect_next_states = [
            ([mv.DOWN], Board([[1, 4, 10, 9], [2, 8, 3, None], [7, 6, 5, 11], [12, 13, 14, 15],])),
            ([mv.LEFT], Board([[1, 4, None, 10], [2, 8, 3, 9], [7, 6, 5, 11], [12, 13, 14, 15],])),
        ]
        next_states = Board(s_init).next_valid_board_states(history)
        self.assertEqual(next_states, expect_next_states)


if __name__ == '__main__':
    unittest.main()
