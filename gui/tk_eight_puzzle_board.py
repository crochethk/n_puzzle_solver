from gui.mock_text import lorem_10ln # TODO TODO TODO remove this later

from tkinter import *
from tkinter import ttk

from eight_puzzle import EightPuzzleBoard
from gui.vec2 import Vec2
from gui.item_highlighter import ItemHighlighter

from tkinter import *


def remove_border(tk_obj: Widget):
    tk_obj.configure({"borderwidth": 0, "highlightthickness": 0}),


class TkGameBoard(Canvas):
    def __init__(self, parent, from_epb: EightPuzzleBoard | None = None, **kwargs):
        field_size = Vec2(80)
        board_size = (field_size * 3) + TkGameBoardField.BORDER_WIDTH

        if from_epb is None:
            # from_state = [[1, 2, 3], [4, None, 6], [7, 8, 9]]
            from_epb = EightPuzzleBoard([[2, 8, 3], [1, 6, 4], [7, None, 5]])

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
                field_val = epb.state[r][c]

                board_fields[c].append(
                    TkGameBoardField(self, pos, field_size, text=f"x: {pos.x}\ny: {pos.y}\nnum: {str(field_val)}"))

                if field_val is None:
                    self.itemconfigure(board_fields[c][r].id, fill="")

        self.fields = board_fields


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

        # transparent box on top. Workaround for cumbersome <Enter>/<Leave> behaviour
        # with "rectangle+text" + deferred eventpropagation on click-hold
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
