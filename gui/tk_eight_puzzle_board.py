from tkinter import *
from tkinter import ttk

from gui.mock_text import lorem_10ln

from eight_puzzle import EightPuzzleBoard
from gui.vec2 import Vec2
from gui.item_highlighter import ItemHighlighter

# WINDOW_POS = Vec2(50, 150)
WINDOW_POS = Vec2(-500, 150)


def remove_border(tk_obj: Widget):
    tk_obj.configure({"borderwidth": 0, "highlightthickness": 0}),


class TkGameBoard(Canvas):
    def __init__(self, parent, from_epb: EightPuzzleBoard | None = None, ** kwargs):
        """
        FIXME: 
        - add arg "board_state" which shall be the initial board_state (see search algos)
        - use that state to initialize the fields accordingly
        """
        field_size = Vec2(80)
        board_size = (field_size * 3) + TkGameBoardField.BORDER_WIDTH

        if from_epb is None:
            # from_state = [[1, 2, 3], [4, None, 6], [7, 8, 9]]
            from_epb = EightPuzzleBoard([[2, 8, 3], [1, 6, 4], [7, None, 5]])
        # state = from_epb.state

        super().__init__(parent, width=board_size.x, height=board_size.y, background="gray75", **kwargs)
        remove_border(self)

        self.set_state(from_epb, field_size)

    def set_state(self, epb: EightPuzzleBoard, field_size: float):
        board_fields: list[list[TkGameBoardField]] = []

        cols = len(epb.state[0])
        rows = len(epb.state)

        for c in range(cols):
            board_fields.append([])
            for r in range(rows):
                pos = field_size * Vec2(c, r)

                # Add numbering
                # num = 1 + c + cols * r
                field_val = epb.state[r][c]

                board_fields[c].append(
                    TkGameBoardField(self, pos, field_size, text=f"x: {pos.x}\ny: {pos.y}\nnum: {str(field_val)}"))

                if field_val is None:
                    self.itemconfigure(board_fields[c][r].id, fill="")

        self.fields = board_fields

    # TODO: add methods specific to board gui behaviour


class TkGameBoardField:
    BORDER_WIDTH = 7

    def __init__(self, parent: TkGameBoard, pos: Vec2, size: Vec2, text=""):
        """
        - `pos` - The positon of the top left corner
        - `size` - Size of the field
        - `test` - Optional text content
        """
        self.parent = parent

        self.bg_color = "light green"
        p1 = pos + Vec2(self.BORDER_WIDTH) // 2
        p2 = p1 + size

        rect_config = (
            (p1.x, p1.y), (p2.x, p2.y),
            {"fill": self.bg_color, "width": self.BORDER_WIDTH}
        )

        # id representing rectangle instance inside parent canvas
        self.id = parent.create_rectangle(*rect_config)

        text_pos = p1 + size / 2
        parent.create_text(text_pos.x, text_pos.y, text=text)

        # transparent box on top, as workaround for cumbersome <Enter>/<Leave>
        # behaviour with "rectangle+text" + deferred eventpropagation on click-hold
        enter_leave_box = parent.create_rectangle(
            *rect_config,
            fill="",
            outline="",
        )

        # hover hightlight effect
        self.highlight = ItemHighlighter(self.parent, self.id, "green")
        parent.tag_bind(enter_leave_box, "<Enter>", self._on_enter)
        parent.tag_bind(enter_leave_box, "<Leave>", self._on_leave)

    def _on_enter(self, ev):
        self.highlight.enable()

    def _on_leave(self, ev):
        self.highlight.disable()

    @property
    def pos(self) -> Vec2:
        """Returns position of top left corner relative to the `parent` canvas."""
        x, y, _, _ = self.parent.coords(self.id)
        return Vec2(x, y)

    @property
    def size(self) -> Vec2:
        """Returns size of this field calculated from `parent` canvas coords."""
        x0, y0, x1, y1 = self.parent.coords(self.id)
        return Vec2(x1, y1) - Vec2(x0, y0)


# ----------- class EightPuzzleGameGui:
def new_game():
    print("click: new game")
    pass


def mk_next_mv():
    print("click: next move")
    pass
# ----------------------


if __name__ == "__main__":
    root = Tk()
    root.title("Eight Puzzle Game")
    # quit on "ESC"
    root.bind("<Escape>", lambda event: root.quit())
    root.bind("<Alt-n>", lambda event: root.quit()) # added for convenience
    root.geometry("+" + str(WINDOW_POS.x) + "+" + str(WINDOW_POS.y))

    main_frame = ttk.Frame(root, padding="3 3 3 3")
    # main_frame = ttk.Frame(root)

    main_frame.grid(
        column=0, row=0,
        # resize mainframe by sticking to all for edges of the grid field
        sticky=NSEW
    )

    # Configure how resizing of "root" propagates to the specified column/row
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Buttons frame
    btns_frame = ttk.Frame(
        main_frame,
        padding=(0, 5, 0, 5) # E,N,W,S
    )
    btns_frame.grid(row=0, column=0, sticky=EW)

    ## btn_new
    ttk.Button(btns_frame, text="New",
               command=new_game
               ).grid(row=0, column=0, sticky=EW)

    ## btn_next_mv
    ttk.Button(btns_frame, text="Next Move",
               command=mk_next_mv).grid(row=0, column=1, sticky=EW)

    btns_frame.columnconfigure(
        list(range(len(btns_frame.grid_slaves(row=0)))), weight=1) #set weight=1 for all columns
    btns_frame.rowconfigure(0, weight=1)

    # board

    # (parent)
    game_board = TkGameBoard(main_frame)
    game_board.grid(row=1, column=0)

    # log frame
    # log_frame = ttk.Frame(main_frame)
    log_frame = ttk.LabelFrame(main_frame, text="Game Log")
    log_frame.grid(row=2, column=0, sticky=NSEW)

    ## log text
    log_text = Text(log_frame, width=40, height=15, relief="sunken")
    log_text.grid(row=0, column=0, sticky=NSEW)

    log_text.insert("1.0", lorem_10ln)
    log_text.configure(state="disabled")

    ## setup vertical scrollbar
    log_sbar = ttk.Scrollbar(log_frame, orient=VERTICAL, command=log_text.yview)
    log_text.configure(yscrollcommand=log_sbar.set)
    log_sbar.grid(row=0, column=2, sticky=NS)

    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)

    # configure main frame grid weights
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(2, weight=1)

    root.mainloop()

    # # # field_size = 80
    # # # board_size = 3 * field_size + 1 # "+1" = "field_borderwidth"
    # # # board_canvas = Canvas(main_frame, width=board_size, height=board_size,
    # # #                       background="gray75", borderwidth=0, highlightthickness=0)
    # # # board_canvas.grid(row=1, column=0)
    # # # board_fields = []
    # # # for i in range(3):
    # # #     board_fields.append([])
    # # #     for j in range(3):
    # # #         p1, p2 = (field_size * i, field_size * j), (field_size * (i + 1), field_size * (j + 1))
    # # #         board_fields[i].append(board_canvas.create_rectangle(*p1, *p2, fill="light green"))
    # # #         # Add numbering
    # # #         num = 1 + i + 3 * j
    # # #         if num == 5: # skip center field
    # # #             continue
    # # #         num = num if num < 5 else num - 1
    # # #         board_canvas.create_text(
    # # #             p1[0] + field_size / 2,
    # # #             p1[1] + field_size / 2,
    # # #             text=str(num)
    # # #         )

    # # # board_canvas.itemconfigure(board_fields[1][1], fill="")
    # # # board_canvas.move(board_fields[0][2], 120, -40)
