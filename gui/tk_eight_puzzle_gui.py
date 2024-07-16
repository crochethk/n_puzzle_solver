from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from eight_puzzle import EightPuzzle
from gui.tk_eight_puzzle_board import TkGameBoard
from gui.mock_text import lorem_10ln # TODO TODO TODO remove this later


class EightPuzzleGui(ttk.Frame):
    def __init__(self, parent, game: EightPuzzle, **kwargs):
        super().__init__(parent, **kwargs)

        #--- Buttons frame
        btns_frame = ttk.Frame(
            self,
            padding=(0, 5, 0, 5) # E,N,W,S
        )
        btns_frame.grid(row=0, column=0, sticky=EW)

        # btn_new
        ttk.Button(btns_frame, text="New",
                   command=self._on_new_game
                   ).grid(row=0, column=0, sticky=EW)

        # btn_next_mv
        ttk.Button(btns_frame, text="Next Move",
                   command=self._on_mk_next_mv).grid(row=0, column=1, sticky=EW)

        btns_frame.columnconfigure(
            list(range(len(btns_frame.grid_slaves(row=0)))), weight=1) #set weight=1 for all columns
        btns_frame.rowconfigure(0, weight=1)

        #--- game board
        self.game = game
        self.board = TkGameBoard(self, self.game.board)
        self.board.grid(row=1, column=0)

        #--- log frame
        log_frame = ttk.LabelFrame(self, text="Game Log")
        log_frame.grid(row=2, column=0, sticky=NSEW)

        self.log_text = ScrolledText(log_frame, width=40, height=15, relief="sunken")
        self.log_text.grid(row=0, column=0, sticky=NSEW)
        self.log_text.insert("1.0", lorem_10ln) #<---------- TODO remove this
        self.log_text.configure(state="disabled")

        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # configure main frame grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

    def _on_new_game(self):
        print("click: new game")
        self.reset_game() #<<<<---- thats what should happen

        # FIXME FIXME FIXME just for memory leak testing
        # Memory leak test
        # # for _ in range(50000):
        # #     # self.board.del_fields()
        # #     self.reset_game()
        # #     insert_text(self.log_text, "1.0", lorem_10ln + "\n")
        # FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME
        pass

    def reset_game(self):
        # - [x] reset gameboard state
        # - [x] reset logging area
        self.board.set_default_state()
        remove_text(self.log_text, "1.0", "end")

    def _on_mk_next_mv(self):
        print("click: next move")
        insert_text(self.log_text, "1.0", "<--- new entry --->\n")

        # FIXME FIXME FIXME just for memory leak testing
        # Memory leak test
        for i in range(50000):
            insert_text(self.log_text, "1.0", f"<--- new entry --->{i + 1}\n")

        # FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME FIXME
        pass


def remove_text(text_w: Text, start_idx: str, end_idx: str):
    # FIXME FIXME FIXME FIXME FIXME FIXME FIXME
    # - we should actually backup text-state and restore it after changing content
    # FIXME FIXME FIXME FIXME FIXME FIXME FIXME
    text_w.configure(state="normal")
    text_w.delete(start_idx, end_idx)
    text_w.configure(state="disabled")


def insert_text(text_w: Text, at_idx: str, the_text: str):
    # FIXME FIXME FIXME FIXME FIXME FIXME FIXME
    # - we should actually backup text-state and restore it after changing content
    # FIXME FIXME FIXME FIXME FIXME FIXME FIXME
    text_w.configure(state="normal")
    text_w.insert(at_idx, the_text)
    text_w.configure(state="disabled")