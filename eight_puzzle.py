import functools
import random
from copy import deepcopy
from enum import Enum

from search_strategy import SearchStrategyBase
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


class EightPuzzleBoard:
    def __init__(self, state: list[list]):
        """
        `state`: 2D-array with "rows x cols"
        """
        self.state = state
        # validate state has an empty field
        _ = self.get_empty_field()

    def __repr__(self) -> str:
        s = ""
        last_i = len(self.state) - 1
        for i, row in enumerate(self.state):
            s += str(row) + ("\n" if i != last_i else "")
        return s

    def clone(self) -> 'EightPuzzleBoard':
        state_clone = deepcopy(self.state)
        return type(self)(state_clone)

    def __eq__(self, other: 'EightPuzzleBoard') -> bool:
        return self.state == other.state

    def get_empty_field(self) -> Vec2:
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
        boards: list[tuple[list[MoveDirection], EightPuzzleBoard]] = []
        empty_pos = self.get_empty_field()

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

    @staticmethod
    def random_board(seed=None) -> 'EightPuzzleBoard':
        random.seed(seed)
        pieces = [1, 2, 3, 4, 5, 6, 7, 8, None]
        random.shuffle(pieces)
        pieces = [pieces[i:i + 3] for i in range(0, 9, 3)]
        return EightPuzzleBoard(pieces)


class EightPuzzle:
    def __init__(
            self,
            initial_board: EightPuzzleBoard,
            goal_board: EightPuzzleBoard,
            search_strategy: SearchStrategyBase):
        self.board = initial_board
        self.goal_board = goal_board
        self.search_strategy = search_strategy

    def __str__(self) -> str:
        """
        Returns a string representation of the puzzle
        """
        s = "--- initial ---\n"
        s += str(self.board)
        s += "\n"
        s += "--- goal ---\n"
        s += str(self.goal_board)
        return s

    def is_goal_board(self, board: EightPuzzleBoard):
        return self.goal_board == board

    def solve(self, exhaustive_search=True) -> list | None:
        """
        Returns a list of solution steps beginning with the first, ending with 
        the last step. They represent the sequence of moves the empty field must
        perform in order to achieve the goal state.
        """

        strategy = self.search_strategy

        strategy.apply([([], self.board)])
        visited = []
        best_history: list[MoveDirection] = None

        counter = 0
        while not strategy.is_done():
            counter += 1

            entry: tuple[list, EightPuzzleBoard] = strategy.pop_state_entry()

            history, state = entry

            best_cost, curr_cost = (
                strategy.path_cost(best_history),
                strategy.path_cost(history)
            )

            if self.is_goal_board(state) \
                    and (best_history is None or best_cost > curr_cost):
                best_history = history
                if exhaustive_search:
                    continue
                else:
                    break

            elif best_history is not None and best_cost < curr_cost:
                # dont branch any deeper, if already found solution is better than current path
                continue

            visited.append(state)
            candidates = state.next_valid_board_states(history)
            candidates = [s for s in candidates if s[1] not in visited]

            self.search_strategy.apply(candidates)

        print(f"Expansions to finish: {counter}")
        return best_history
