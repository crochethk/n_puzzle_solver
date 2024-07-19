import threading
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from eight_puzzle import EightPuzzle, MoveDirection
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

    def enable_all(self):
        for btn_id in self.buttons.keys():
            self.enable_btn(btn_id)

    def disable_all(self):
        for btn_id in self.buttons.keys():
            self.disable_btn(btn_id)


class EightPuzzleGui(ttk.Frame):
    def __init__(self, parent, game: EightPuzzle, **kwargs):
        super().__init__(parent, **kwargs)

        # counter for steps performed so far
        self._step_cnt = 0

        #--- Buttons frame
        self.controls_panel = GameControls(
            self,
            padding=(0, 5, 0, 5) # E,N,W,S
        )
        self.controls_panel.grid(row=0, column=0, columnspan=999, sticky=NSEW)

        self.controls_panel.add_button("restart", "Restart", self._on_restart_game)
        self.controls_panel.add_button("next", "Next Move", self._on_mk_next_mv)
        self.controls_panel.add_button("new", "New", self._on_new_game)
        self.controls_panel.add_button("cancel_solve", "Cancel", self._on_cancel_solve)
        self.controls_panel.build()

        #--- Game board
        self.game = game

        self.board = TkGameBoard(self, self.game.board)
        self.board.grid(row=10, column=0, sticky=E, padx=2)

        self.goal_b = TkGameBoard(self, self.game.goal_board)
        self.goal_b.grid(row=10, column=1, sticky=W, padx=2)

        #--- Log panel
        self.log_panel = InteractionLogPanel(self, "Game Log", 10, 15)
        self.log_panel.grid(row=20, column=0, columnspan=999, sticky=NSEW) # dirty: span all cols
        self.rowconfigure(20, weight=1)

        #--- Progress bar
        self.prog_bar = ttk.Progressbar(self, mode="indeterminate")
        self.prog_bar.grid(row=30, column=0, columnspan=999, sticky=NSEW)
        self.rowconfigure(30, minsize=25)

        self.columnconfigure((0, 1), weight=1)

        self.log_panel.add_message("<--- Start --->")
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
        self._step_cnt = 0
        self.controls_panel.disable_btn("next")
        self.controls_panel.disable_btn("restart")
        self.controls_panel.disable_btn("new")
        if self.game.is_solvable():
            self.log_panel.add_message("Solving puzzle. This may take some time...")
            self.start_progress_bar()
            threading.Thread(target=self.solve_puzzle_in_thread, daemon=True).start()
        else:
            self.log_panel.add_message(f"Unsolvable configuration. Try another!")
            self.controls_panel.enable_btn("new")

    def start_progress_bar(self):
        self.prog_bar.start(25) # determines move speed
        self.prog_bar.grid_configure()

    def stop_progress_bar(self):
        self.prog_bar.stop()
        self.prog_bar.grid_remove()

    def solve_puzzle_in_thread(self):
        print(f"{threading.currentThread().getName()}")
        solution = self.game.solve(exhaustive_search=True) # FIXME `True` for trying out progressbar
        self.after(0, self.update_ui_with_solution, solution)
        self.after(0, self.stop_progress_bar)

    def update_ui_with_solution(self, solution: list[MoveDirection]):
        self.log_panel.add_message(f"{len(solution)} steps until solved.")
        self.controls_panel.enable_all()

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
            self._step_cnt += 1
            self.game.board.mv_empty(next_step)
            self.board.set_state(self.game.board)
            self.log_panel.add_message(f"{self._step_cnt:<3} Move: {next_step.__repr__()}")

        if self.game.is_win():
            self.log_panel.add_message("<--- DONE! --->")
            self.controls_panel.disable_btn("next")

    def _on_cancel_solve(self):
        # TODO Must implement "solver thread" in the actual game first
        # TODO since we need a way to send and check events to the worker thread
        # TODO as of now we have no control about, what the solver is doing from
        # TODO inside the ui
        # TODO
        # TODO Outline to achive this:
        # TODO      - it shall get an additional lambda argument upon creation,
        # TODO          that returns a bool from main thread
        # TODO      - add check whehter the lambda returns True (stop)
        # TODO      - gui can then "set" the according bool, to signal worker to stop
        pass


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
