from queue import Queue, LifoQueue, PriorityQueue


class SearchStrategyBase:
    """
    Base class for search strategies. A `SearchStrategy` basically manages
    the 'state expansion queue'.
    """

    def __init__(self, queue: Queue):
        self.queue = queue

    def apply(self, new_state_entries: list[tuple[list, any]]):
        """
        Adds all state entries from `new_state_entries` to the expansion queue.

        Each `entry` should be a tuple of past steps, to calculate current costs with 
        and the associated state.
        """
        for s in new_state_entries:
            self.add_state_entry(s)

    def is_done(self) -> bool:
        """
        Returns, if there are any pending entries to expand.
        """
        return self.queue.empty()

    def add_state_entry(self, entry):
        """
        Adds an entry to the queue, obeying to the strategies inserting order.
        """
        self.queue.put(entry)

    def pop_state_entry(self) -> any:
        """
        Returns next entry and removes it from the underlying queue.
        """
        return self.queue.get()

    def path_cost(self, history: list):
        return 0 if history is None else len(history)

    def reset(self):
        """
        Resets internal state of this strategy, so it can be reused again.
        """
        self.queue = self.queue.__class__()


class DepthFirstSearch(SearchStrategyBase):
    """
    Inserts expanded state entries to the start of the expansion queue.
    """

    def __init__(self):
        super().__init__(LifoQueue())


class BreadthFirstSearch(SearchStrategyBase):
    """
    Appends expanded state entries to the end of the expansion queue.
    """

    def __init__(self):
        super().__init__(Queue())


class AStarSearch(SearchStrategyBase):
    """
    A strategy aimed for `A*` search implementation. Internally utilizes a priority
    queue. Requires the target/goal state and a fitting heuristic function upon creation.

    Maintains a PriorityQueue of tuples, where first element is the priority (based on
    the state's approx. costs) and the second element is the usual entry consisting
    of a list (e.g. move history) and the actual state.
    """

    def __init__(self, goal_state, heuristic_fn):
        super().__init__(PriorityQueue())

        self.goal = goal_state
        # function that given an input state and the goal state returns a rating for input
        self.hfn = heuristic_fn

    def apply(self, new_state_entries: list):
        for entry in new_state_entries:
            history, state = entry
            approx_cost = self.approx_cost(history, state)
            self.add_state_entry((approx_cost, entry))

    def pop_state_entry(self) -> any:
        _, entry = self.queue.get()
        return entry

    def approx_cost(self, history: list, state):
        return self.path_cost(history) + self.hfn(state, self.goal)
