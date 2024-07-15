from tkinter import *
from tkinter import ttk

from mock_text import lorem_10ln

from vec2 import *

# WINDOW_POS = Vec2(50, 150)
WINDOW_POS = Vec2(-500, 150)


def remove_border(tk_obj: Widget):
    tk_obj.configure({"borderwidth": 0, "highlightthickness": 0}),


class GameBoard(Canvas):
    def __init__(self, parent, **kwargs):
        """
        FIXME: 
        - add arg "board_state" which shall be the initial board_state (see search algos)
        - use that state to initialize the fields accordingly
        """
        field_size = Vec2(80)
        board_size = (field_size * 3) + GameBoardField.BORDER_WIDTH

        super().__init__(parent, width=board_size.x, height=board_size.y, background="gray75", **kwargs)
        remove_border(self)

        board_fields: list[list[GameBoardField]] = []

        cols = range(3)
        rows = range(3)

        for i in cols:
            board_fields.append([])
            for j in rows:
                pos = field_size * Vec2(i, j)

                # Add numbering
                num = 1 + i + 3 * j

                # skip center field
                num = "" if num == 5 else (num if num < 5 else num - 1)
                # # if num == 5:
                # #     continue
                # # num = num if num < 5 else num - 1

                board_fields[i].append(
                    GameBoardField(self, pos, field_size, text=f"x: {pos.x}\ny: {pos.y}\nnum: {str(num)}"))

        self.fields = board_fields
        self.itemconfigure(board_fields[1][1].id, fill="")
        # board_canvas.move(board_fields[0][2], 120, -40)

        # TODO TODO TODO
        # add event listeners, e.g.
        #     ```py
        #     self.bind("<Button-1>", self.save_posn)
        #     self.bind("<B1-Motion>", self.add_line)
        #     ```

    # TODO: add methods specific to board gui behaviour


class GameBoardField:
    BORDER_WIDTH = 7

    def __init__(self, parent: GameBoard, pos: Vec2, size: Vec2, text=""):
        """
        - `pos` - The positon of the top left corner
        - `size` - size of the field
        """
        self.parent = parent

        p1 = pos + Vec2(self.BORDER_WIDTH) // 2
        p2 = p1 + size

        # id representing rectangle instance inside parent
        self.id = self.parent.create_rectangle(
            (p1.x, p1.y), (p2.x, p2.y),
            fill="light green",
            activefill="green",
            width=self.BORDER_WIDTH
        )

        text_pos = p1 + size / 2
        self.parent.create_text(
            text_pos.x,
            text_pos.y,
            text=text
        )

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
    game_board = GameBoard(main_frame)
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
