from tkinter import *

import n_puzzle_heuristics as heuristics
from gui.tk_n_puzzle_gui import NPuzzleGUI
from n_puzzle import NPuzzleGame, NPuzzleBoard
from search_strategy import AStarSearch
from vec2 import Vec2

from n_puzzle_solver import NPuzzleSolver

# TODO
# SEED = 42
# SEED = None

# THE_INITIAL_BOARD = NPuzzleBoard.random_board(SEED)
THE_INITIAL_BOARD = NPuzzleBoard([[2, 8, 3], [1, 6, 4], [7, None, 5]])
THE_GOAL_BOARD = NPuzzleBoard([[1, 2, 3], [8, None, 4], [7, 6, 5]])
THE_STRATEGY = AStarSearch(THE_GOAL_BOARD, heuristics.cumulative_distance)

WINDOW_POS = Vec2(50, 150)
# WINDOW_POS = Vec2(-500, 150)


if __name__ == "__main__":
    root = Tk()
    root.title(f"{THE_INITIAL_BOARD.N} Puzzle Game")
    # quit on "ESC"
    root.bind("<Escape>", lambda ev: root.quit())
    root.bind("<F5>", lambda ev: root.quit()) # added for convenience
    root.geometry("+" + str(WINDOW_POS.x) + "+" + str(WINDOW_POS.y))

    game = NPuzzleGame(THE_INITIAL_BOARD, THE_GOAL_BOARD)
    solver = NPuzzleSolver(game, THE_STRATEGY)

    game_gui = NPuzzleGUI(root, game, solver, padding="3 3 3 3")
    # Place game_gui in col=0, row=0 in the parent's (root) grid,
    # sticking to all four egdes of the cell, when grid is resized
    game_gui.grid(column=0, row=0, sticky=NSEW)

    # Configure how resizing of "root" propagates to the specified column/row
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # <field_w, field_h> * <cols, rows> * <some factor>
    win_min_size = (
        game_gui.board.field_size
        * Vec2(len(game.board.state[0]), len(game.board.state))
        * Vec2(2.1, 2)
    )
    root.minsize(width=int(win_min_size.x), height=int(win_min_size.y))

    root.mainloop()
