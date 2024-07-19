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
        _ = self.empty_field_pos()

    def __repr__(self) -> str:
        s = "["
        last_i = len(self.state) - 1
        for i, row in enumerate(self.state):
            s += str(row) + ("," if i != last_i else "]")
        return s

    def clone(self) -> 'EightPuzzleBoard':
        state_clone = deepcopy(self.state)
        return type(self)(state_clone)

    def __eq__(self, other: 'EightPuzzleBoard') -> bool:
        return self.state == other.state

    def __hash__(self) -> int:
        tp_state = tuple(tuple(row) for row in self.state)
        return hash(tp_state)

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
        boards: list[tuple[list[MoveDirection], EightPuzzleBoard]] = []
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
    def random_board(seed=None) -> 'EightPuzzleBoard':
        random.seed(seed)
        pieces = [1, 2, 3, 4, 5, 6, 7, 8, None]
        random.shuffle(pieces)
        pieces = [pieces[i:i + 3] for i in range(0, 9, 3)]
        return EightPuzzleBoard(pieces)


class EightPuzzle: # TODO could or should be split up into "EightPuzzleSolver" and "EightPuzzleGame"
    def __init__(
            self,
            initial_board: EightPuzzleBoard,
            goal_board: EightPuzzleBoard,
            search_strategy: SearchStrategyBase):
        self.board = initial_board
        self.goal_board = goal_board
        self.search_strategy = search_strategy
        self.solution = None
        self.start_board = initial_board.clone()

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

    def solve(self, exhaustive_search=False) -> list | None:
        """
        Returns a list of solution steps and stores it in `self.solution`.
        The list starts with the first and ends with the last step/move the empty 
        field must perform in order to achieve the goal state.
        Returns/stores `None`, in case the puzzle is not solvable, i.e. start 
        configuration can't be transformed into goal configuration.
        """

        if not self.is_solvable():
            self.solution = None
            return None

        strategy = self.search_strategy

        strategy.apply([([], self.board)])
        visited = set()
        best_history: list[MoveDirection] = None

        counter = 0
        while not strategy.is_done():
            counter += 1

            entry: tuple[list, EightPuzzleBoard] = strategy.pop_state_entry()

            history, state = entry
            visited.add(state)

            best_cost, curr_cost = (
                strategy.path_cost(best_history),
                strategy.path_cost(history)
            )

            if self.goal_board == state \
                    and (best_history is None or best_cost > curr_cost):
                best_history = history
                if exhaustive_search:
                    continue
                elif len(best_history) == 0:
                    # start state is goal_state, cant get better than that
                    break
                else:
                    break

            elif best_history is not None and best_cost < curr_cost:
                # dont branch any deeper, if already found solution is better than current path
                continue

            candidates = state.next_valid_board_states(history)
            candidates = [(h, s) for h, s in candidates if s not in visited]

            strategy.apply(candidates)

        print(f"Expansions to finish: {counter}")
        self.solution = best_history
        return best_history

    def is_win(self) -> bool:
        return self.board == self.goal_board

    def is_solvable(self) -> bool:
        """
        Checks whether the current game is solvable, i.e. if current `board` state
        can be tranformed into the `goal_board`.
        1) Determine parity of goal_board from steps count, the empty field 
            has to perform to reach its target
        2) Determine parity of transformation steps of `start` into `goal` using 
            transpositions (i.e. swapping) only
        3) Parities must match in order for the configuration to be solvable.
        """

        # Determine "goal parity"
        empty_start_pos = self.board.empty_field_pos()
        empty_goal_pos = self.goal_board.empty_field_pos()
        # ODD => 1, EVEN => 0
        parity_goal = self.board.step_distance(empty_start_pos, empty_goal_pos) % 2

        # Determine "start board parity"
        def flatten(arr): return [val for row in arr for val in row]
        start = flatten(self.board.state)
        goal = flatten(self.goal_board.state)

        swaps_count = 0
        for goal_i, v in enumerate(goal):
            # Example: goal_i=2
            #  goal: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            #        .......^
            # start: [1, 2, 7, 5, 0, 4, 6, 8, 3]
            #               ^←             ← ^^^(start_i=8)
            # -> swap start[2] and start[8]
            try:
                start_i = start.index(v)
            except ValueError:
                # start/goal with missing value is not solvable for
                return False

            if goal_i != start_i:
                # swap elements
                swaps_count += 1
                tmp = start[goal_i]
                start[goal_i] = start[start_i]
                start[start_i] = tmp
            else:
                # already on correct pos
                continue
        parity_current = swaps_count % 2
        return parity_goal == parity_current

    def renew_game(self, new_start: EightPuzzleBoard = None, new_goal: EightPuzzleBoard = None):
        """
        Resets this puzzle intance and its solver.
        - If `new_start` board is not provided a randomized will be set, otherwise `new_start`
            will used.
        - If `new_goal` is not provided the current `goal_board` is preserved.
        """
        self.solution = None
        self.board = EightPuzzleBoard.random_board() if new_start is None else new_start
        self.start_board = self.board.clone()
        self.search_strategy.reset()
        self.goal_board = self.goal_board if new_goal is None else new_goal

    def next_solution_step(self):
        if self.solution is None:
            raise AssertionError(
                "`solve()` method must be run at least once before querying next step"
            )
        return self.solution.pop(0) if len(self.solution) > 0 else None
