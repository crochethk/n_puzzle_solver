"""
Solver for a "N Puzzle Game". Although it finds a solution, if there is any,
it can take rather long (>30min) when used with puzzles greater than 3x3.
One reason beeing, that a 4x4 board ("15 Puzzle") has `16!/9! = 57.657.600` times (!)
the amount of permutations a 3x3 board has.
"""

from n_puzzle import NPuzzleBoard, NPuzzleGame, MoveDirection
from search_strategy import SearchStrategyBase


class NPuzzleSolver:
    def __init__(self, game: NPuzzleGame, search_strategy: SearchStrategyBase):
        self.game = game
        self.search_strategy = search_strategy
        self.solution = None

    def solve(self, exhaustive_search=False) -> list | None:
        """
        Returns a list of solution steps and stores it in `self.solution`.
        The list starts with the first and ends with the last step/move the empty 
        field must perform in order to achieve the goal state.
        Returns/stores `None`, in case the puzzle is not solvable, i.e. start 
        configuration can't be transformed into goal configuration.
        """
        self.reset()

        if not self.is_solvable(self.game):
            return None

        strategy = self.search_strategy

        strategy.apply([([], self.game.board)])
        visited = set()
        best_history: list[MoveDirection] = None

        counter = 0
        while not strategy.is_done():
            counter += 1

            entry: tuple[list, NPuzzleBoard] = strategy.pop_state_entry()

            history, state = entry
            visited.add(state)

            best_cost, curr_cost = (
                strategy.path_cost(best_history),
                strategy.path_cost(history)
            )

            if self.game.goal_board == state \
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

    @staticmethod
    def is_solvable(game: NPuzzleGame) -> bool:
        """
        Checks whether the current game is solvable, i.e. if its `board` state
        can be tranformed into the `goal_board`.
        1) Determine parity of goal_board from steps count, the empty field 
            has to perform to reach its target
        2) Determine parity of transformation steps of `start` into `goal` using 
            transpositions (i.e. swapping) only
        3) Parities must match in order for the configuration to be solvable.
        """

        # Determine "goal parity"
        empty_start_pos = game.board.empty_field_pos()
        empty_goal_pos = game.goal_board.empty_field_pos()
        # ODD => 1, EVEN => 0
        parity_goal = game.board.step_distance(empty_start_pos, empty_goal_pos) % 2

        # Determine "start board parity"
        def flatten(arr): return [val for row in arr for val in row]
        start = flatten(game.board.state)
        goal = flatten(game.goal_board.state)

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
        parity_start = swaps_count % 2
        return parity_goal == parity_start

    def next_solution_step(self):
        if self.solution is None:
            raise AssertionError(
                "`solve()` method must be run at least once before querying next step"
            )
        return self.solution.pop(0) if len(self.solution) > 0 else None

        # TODO we could change solution, so it is not "popped" instead hold an appropriate iter instance
        # TODO that way we also needn't to recalculate on reset
        # TODO also this would probably allow telling, which step we are in

    def reset(self):
        """Resets this solver to its initial state."""
        self.solution = None
        self.search_strategy.reset()
