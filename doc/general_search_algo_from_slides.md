- Pseudo Code of a general search algorithm
    ```py
    def search(start, expand, strategy, is_goal):
        queue=[start]
        reached=[]
        while queue:
            state = queue.pop()
            if is_goal(state):
                return state  # eine Lösung
            reached.push(state)
            ex = expand(state, ops)
            newex = [s for s in ex if s not in reached]
            queue = strategy(queue, newex)
        return None
    ```
    - `ops`:
        - set of operations, that define ways to derive the next "state-candidates" (`ex`) from the current state
    - `strategy`:
        - decides, where or how the newly derived states are put into the queue (start/end/prioritized/...)