from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from eight_puzzle import EightPuzzle
from gui.tk_eight_puzzle_board import TkGameBoard


class InteractionLogPanel(ttk.LabelFrame):
    def __init__(self, parent, label, text_width, text_height, **kwargs):
        """
        - `label`: the label of the panel.
        - `text_width` and `text_height`: the initial width and height of the textarea.
        """
        super().__init__(parent, text=label, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.text_area = ScrolledText(self, width=text_width, height=text_height, relief="sunken")
        self.text_area.grid(row=0, column=0, sticky=NSEW)
        self.text_area.configure(state="disabled")

    def add_message(self, msg: str):
        """Adds the given message to the log panel."""
        insert_text(self.text_area, "1.0", f"{msg}\n")

    def clear_log(self):
        """Removes all messages from the log panel."""
        remove_text(self.text_area, "1.0", "end")


class GameControls(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.next_col_num = 0
        self.buttons: dict[str, ttk.Button] = dict()

    def next_column_number(self) -> int:
        num = self.next_col_num
        self.next_col_num += 1
        return num

    def add_button(self, id: str, label: str, command, **btn_config):
        """
        Adds a new button. If a button already exists with the `id`, it will be replaced.
        - `id`: Name which will be used to refer to the new button if needed.
        - `label`: Text to display on the button.
        - `command`: Function to execute when button is pressed.
        """
        btn = ttk.Button(self, text=label, command=command, **btn_config)
        btn.grid(row=0, column=self.next_column_number(), sticky=EW)
        self.buttons[id] = btn

    def build(self):
        #set weight=1 for all columns
        self.columnconfigure(
            list(range(len(self.grid_slaves(row=0)))), weight=1)
        self.rowconfigure(0, weight=1)

    def disable_btn(self, id: str):
        """Disables button with id `id`. Does nothing if `id` is unknown."""
        btn = self.buttons.get(id)
        if btn:
            btn.configure(state="disabled")

    def enable_btn(self, id: str):
        """Enables button with id `id`. Does nothing if `id` is unknown."""
        btn = self.buttons.get(id)
        if btn:
            btn.configure(state="normal")


class EightPuzzleGui(ttk.Frame):
    def __init__(self, parent, game: EightPuzzle, **kwargs):
        super().__init__(parent, **kwargs)

        #--- Buttons frame
        self.controls_panel = GameControls(
            self,
            padding=(0, 5, 0, 5) # E,N,W,S
        )
        self.controls_panel.grid(row=0, column=0, sticky=EW)

        self.controls_panel.add_button("new", "New", self._on_new_game)
        self.controls_panel.add_button("restart", "Restart", self._on_restart_game)
        self.controls_panel.add_button("next", "Next Move", self._on_mk_next_mv)
        self.controls_panel.build()

        #--- Game board
        self.game = game
        self.board = TkGameBoard(self, self.game.board)
        self.board.grid(row=1, column=0)

        goalb = TkGameBoard(self, self.game.goal_board)
        goalb.grid(row=1, column=1)

        #--- Log panel
        self.log_panel = InteractionLogPanel(self, "Game Log", 40, 15)
        self.log_panel.grid(row=2, column=0, columnspan=999, sticky=NSEW) # dirty: span all cols

        # configure main frame grid weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.prepare_game()

    def _on_restart_game(self):
        self.restart_game()
        self.log_panel.add_message("<--- Game restarted --->")
        self.prepare_game()

    def _on_new_game(self):
        self.new_random_game()
        self.log_panel.add_message("<--- New game started --->")
        self.prepare_game()

    def prepare_game(self):
        """Prepares the game for user interaction."""
        self.controls_panel.disable_btn("next")
        if self.game.is_solvable():
            hist = self.game.solve(exhaustive_search=False)
            self.log_panel.add_message(f"{len(hist)} steps until solved.")
            self.controls_panel.enable_btn("next")
        else:
            self.log_panel.add_message(f"Unsolvable configuration. Try another!")

    def restart_game(self):
        self.log_panel.clear_log()
        self.game.renew_game(self.game.start_board)
        self.board.set_state(self.game.board)

    def new_random_game(self):
        self.log_panel.clear_log()
        self.game.renew_game()
        self.board.set_state(self.game.board)

    def _on_mk_next_mv(self):
        next_step = self.game.next_solution_step()
        if next_step is not None:
            self.game.board.mv_empty(next_step)
            self.board.set_state(self.game.board)
            self.log_panel.add_message(f"Move: {next_step.__repr__()}")

        if self.game.is_win():
            self.log_panel.add_message("<--- DONE! --->")
            self.controls_panel.disable_btn("next")


def remove_text(text_w: Text, start_idx: str, end_idx: str):
    original = text_w["state"]
    text_w.configure(state="normal")
    text_w.delete(start_idx, end_idx)
    text_w.configure(state=original)


def insert_text(text_w: Text, at_idx: str, the_text: str):
    original = text_w["state"]
    text_w.configure(state="normal")
    text_w.insert(at_idx, the_text)
    text_w.configure(state=original)
