from tkinter import *

import eight_puzzle_heuristics as ep_heurs
from eight_puzzle import EightPuzzle, EightPuzzleBoard
from gui.tk_eight_puzzle_gui import EightPuzzleGui
from search_strategy import AStarSearch
from vec2 import Vec2


SEED = 42
# SEED = None
# THE_INITIAL_BOARD = EightPuzzleBoard.random_board(SEED)
THE_INITIAL_BOARD = EightPuzzleBoard([[2, 8, 3], [1, 6, 4], [7, None, 5]])
THE_GOAL_BOARD = EightPuzzleBoard([[1, 2, 3], [8, None, 4], [7, 6, 5]])
THE_STRATEGY = AStarSearch(THE_GOAL_BOARD, ep_heurs.cumulative_distance)

# WINDOW_POS = Vec2(50, 150)
WINDOW_POS = Vec2(-500, 150)


if __name__ == "__main__":
    root = Tk()
    root.title("Eight Puzzle Game")
    # quit on "ESC"
    root.bind("<Escape>", lambda ev: root.quit())
    root.bind("<Alt-n>", lambda ev: root.quit()) # added for convenience
    root.bind("<F5>", lambda ev: root.quit()) # added for convenience
    root.geometry("+" + str(WINDOW_POS.x) + "+" + str(WINDOW_POS.y))

    # Configure how resizing of "root" propagates to the specified column/row
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    game = EightPuzzle(THE_INITIAL_BOARD, THE_GOAL_BOARD, THE_STRATEGY)
    game_gui = EightPuzzleGui(root, game, padding="3 3 3 3")
    # Place game_gui in col=0, row=0 in the parent's (root) grid,
    # sticking to all four egdes of the cell, when grid is resized
    game_gui.grid(column=0, row=0, sticky=NSEW)

    root.mainloop()
