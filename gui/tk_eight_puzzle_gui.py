from gui.tk_eight_puzzle_board import TkGameBoard
from gui.mock_text import lorem_10ln # TODO TODO TODO remove this later

from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


class EightPuzzleGui(ttk.Frame):
    def __init__(self, parent, **kwargs):
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
        self.board = TkGameBoard(self)
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
        pass

    def _on_mk_next_mv(self):
        print("click: next move")
        pass
