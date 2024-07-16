from gui.tk_eight_puzzle_board import EightPuzzleGui, TkGameBoard
from gui.vec2 import Vec2
from tkinter import *
from tkinter import ttk

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

    game_gui = EightPuzzleGui(root, padding="3 3 3 3")
    # Place game_gui in col=0, row=0 in the parent's (root) grid,
    # sticking to all four egdes of the cell, when grid is resized
    game_gui.grid(column=0, row=0, sticky=NSEW)

    root.mainloop()
