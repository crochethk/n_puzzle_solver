import functools
import random
from copy import deepcopy
from enum import Enum
from math import sqrt
from vec2 import Vec2


@functools.total_ordering
class MoveDirection(Enum):
    DOWN = Vec2(1, 0)
    UP = Vec2(-1, 0)
    RIGHT = Vec2(0, 1)
    LEFT = Vec2(0, -1)

    def __repr__(self) -> str:
        return self.name.lower()

    def __lt__(self, other):
        # quick 'n dirty...
        return self.value._coords.__lt__(other.value._coords)


class NPuzzleBoard:
    def __init__(self, state: list[list]):
        """
        `state`: 2D-array with "rows x cols"
        """
        self.state = state
        # validate state has an empty field
        _ = self.empty_field_pos()

    def __repr__(self) -> str:
        s = "["
        last_i = len(self.state) - 1
        for i, row in enumerate(self.state):
            s += str(row) + ("," if i != last_i else "]")
        return s

    def clone(self) -> 'NPuzzleBoard':
        state_clone = deepcopy(self.state)
        return type(self)(state_clone)

    def __eq__(self, other: 'NPuzzleBoard') -> bool:
        return self.state == other.state

    def __hash__(self) -> int:
        tp_state = tuple(tuple(row) for row in self.state)
        return hash(tp_state)

    @property
    def N(self) -> int:
        return len(self.state)**2 - 1

    def empty_field_pos(self) -> Vec2:
        """
        Returns the position of the empty field.
        """
        empty_pos = self.get_pos_of(None)
        if empty_pos is None:
            raise ValueError("no empty field found in puzzle board state")
        else:
            return empty_pos

    def next_valid_board_states(self, mv_history: list[MoveDirection]):
        """
        Returns list of pairs `(<mv_history>, <new_board>)`, where:
        - `mv_history` is the given `mv_history` with the move which led to
            `new_board` appended.
        - `new_board` is a board instance representing a possible next state.
        """
        boards: list[tuple[list[MoveDirection], NPuzzleBoard]] = []
        empty_pos = self.empty_field_pos()

        for mv_dir in MoveDirection:
            target_pos = empty_pos + mv_dir.value

            if self.contains_pos(target_pos):
                new_board = self.clone()
                # switch target and empty fields
                new_board.swap_fields(empty_pos, target_pos)
                mv_hist = mv_history.copy()
                mv_hist.append(mv_dir)
                boards.append((mv_hist, new_board))
        return boards

    def swap_fields(self, field_1: Vec2, field_2: Vec2) -> None:
        """
        Swaps content of field at `field_1` with `field_2`'s.
        """
        f1_row, f1_col = (field_1.x, field_1.y)
        f2_row, f2_col = (field_2.x, field_2.y)
        f1_tmp = self.state[f1_row][f1_col]
        self.state[f1_row][f1_col] = self.state[f2_row][f2_col]
        self.state[f2_row][f2_col] = f1_tmp

    def contains_pos(self, position: Vec2):
        r, c = (position.x, position.y)
        return (r >= 0 and r < len(self.state) and
                c >= 0 and c < len(self.state[0]))

    def get_pos_of(self, target) -> Vec2 | None:
        for row_idx, row in enumerate(self.state):
            try:
                col_idx = row.index(target)
                return Vec2(row_idx, col_idx)
            except ValueError:
                continue
        return None

    def mv_empty(self, mv_dir: MoveDirection):
        """
        Moves empty field in `mv_dir`. If it's not a valid move, it is silently 
        ignored.
        """
        empty_pos = self.empty_field_pos()
        target_pos = empty_pos + mv_dir.value
        if self.contains_pos(target_pos):
            self.swap_fields(empty_pos, target_pos)

    @staticmethod
    def step_distance(pos1: Vec2, pos2: Vec2):
        """
        Returns distance as the sum of gridsteps required from `pos1` to `pos2`.
        """
        direction = pos2 - pos1
        return abs(direction.x) + abs(direction.y)

    @staticmethod
    def random_board(seed=None, n_pieces: int = 8) -> 'NPuzzleBoard':
        """
        Creates a new board with randomized fields.
        - `n_pieces`: specifies the number of "pieces" on the board, e.g. `8` for an 8-Puzzle-Board
        """
        random.seed(seed)
        pieces = list(range(1, n_pieces + 1))
        pieces.append(None)
        random.shuffle(pieces)
        size = int(sqrt(n_pieces + 1))
        pieces = [pieces[i:i + size] for i in range(0, n_pieces + 1, size)]
        return NPuzzleBoard(pieces)


class NPuzzleGame:
    def __init__(self, start_board: NPuzzleBoard, goal_board: NPuzzleBoard):
        self.board = start_board
        self.goal_board = goal_board
        self.start_board = start_board.clone()

    def __str__(self) -> str:
        """
        Returns a string representation of the puzzle
        """
        s = "--- start ---\n"
        s += str(self.start_board)
        s += "\n"
        s += "--- current ---\n"
        s += str(self.board)
        s += "\n"
        s += "--- goal ---\n"
        s += str(self.goal_board)
        return s

    def is_win(self) -> bool:
        return self.board == self.goal_board

    def renew(self, new_start: NPuzzleBoard = None, new_goal: NPuzzleBoard = None):
        """
        Resets this puzzle intance to its initial state.
        - If `new_start` board is not provided a randomized will be created, otherwise `new_start`
            will be used.
        - If `new_goal` is not provided the current `goal_board` is preserved.
        """
        self.board = NPuzzleBoard.random_board(n_pieces=self.board.N) if new_start is None else new_start
        self.start_board = self.board.clone()
        self.goal_board = self.goal_board if new_goal is None else new_goal
