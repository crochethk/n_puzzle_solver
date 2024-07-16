from tkinter import *

from eight_puzzle import EightPuzzleBoard
from gui.item_highlighter import ItemHighlighter
from vec2 import Vec2


def remove_border(tk_obj: Widget):
    tk_obj.configure({"borderwidth": 0, "highlightthickness": 0}),


FIELD_BG_CLR = "light green"
FIELD_HL_CLR = "green"


class TkGameBoard(Canvas):
    default_epb = EightPuzzleBoard([[2, 8, 3], [1, 6, 4], [7, None, 5]])

    def __init__(self, parent, from_epb: EightPuzzleBoard | None = None, **kwargs):
        self.field_size = Vec2(80)
        board_size = (self.field_size * 3) + TkGameBoardField.BORDER_WIDTH

        super().__init__(parent, width=board_size.x, height=board_size.y, background="gray75", **kwargs)
        remove_border(self)

        if from_epb is None:
            # from_state = [[1, 2, 3], [4, None, 6], [7, 8, 9]]
            from_epb = self.__class__.default_epb

        # Init empty fields
        epb = from_epb
        self.fields: list[list[TkGameBoardField]] = []

        cols = len(epb.state[0])
        rows = len(epb.state)

        for c in range(cols):
            self.fields.append([])
            for r in range(rows):
                pos = self.grid_position(c, r)
                self.fields[c].append(
                    TkGameBoardField(self, pos, self.field_size, from_epb.state[c][r]))

        # Configure fields according to `from_epb`
        self.set_state(from_epb)

    def grid_position(self, col, row) -> Vec2:
        return self.field_size * Vec2(col, row)

    def set_default_state(self):
        self.set_state(self.__class__.default_epb)

    def set_state(self, epb: EightPuzzleBoard):
        """
        Reconfigures this canvas's items to match state represented by `epb`.
        """
        cols = len(epb.state[0])
        rows = len(epb.state)

        for c in range(cols):
            for r in range(rows):
                field_val = epb.state[r][c]
                f = self.fields[c][r]
                f.set_value(field_val)


class TkGameBoardField:
    BORDER_WIDTH = 7

    def set_value(self, value: int | None):
        """
        Sets this field's value, which decides about text and appearance.
        """
        bg_color = "" if value is None else FIELD_BG_CLR
        self.parent.itemconfigure(self.bg_id, fill=bg_color)
        pos = self.pos
        self.parent.itemconfigure(self.txt_id, text=f"x: {pos.x}\ny: {pos.y}\nnum: {str(value)}")

    def __init__(self, parent: TkGameBoard, pos: Vec2, size: Vec2, value: int | None):
        """
        - `pos` - The positon of the top left corner
        - `size` - Size of the field
        - `value` - The value this field should represent
        """
        self.parent = parent

        p1 = pos + Vec2(self.BORDER_WIDTH) // 2
        p2 = p1 + size

        rect_config = (
            (p1.x, p1.y), (p2.x, p2.y),
            {"width": self.BORDER_WIDTH}
        )

        # id representing bg rectangle instance inside parent canvas
        self.bg_id: int = parent.create_rectangle(*rect_config)

        text_pos = p1 + size / 2
        self.txt_id: int = parent.create_text(text_pos.x, text_pos.y)

        # transparent box on top. Workaround for cumbersome <Enter>/<Leave> behaviour
        # with "rectangle+text" + deferred eventpropagation on click-hold
        enter_leave_box = parent.create_rectangle(
            *rect_config,
            fill="",
            outline=""
        )

        self.set_value(value)

        # hover hightlight effect
        self.highlight = ItemHighlighter(self.parent, self.bg_id, FIELD_HL_CLR)
        parent.tag_bind(enter_leave_box, "<Enter>", self._on_enter)
        parent.tag_bind(enter_leave_box, "<Leave>", self._on_leave)

    def _on_enter(self, ev):
        self.highlight.enable()

    def _on_leave(self, ev):
        self.highlight.disable()

    @property
    def pos(self) -> Vec2:
        """Returns position of top left corner relative to the `parent` canvas."""
        x, y, _, _ = self.parent.coords(self.bg_id)
        return Vec2(x, y)

    # # # @property
    # # # def size(self) -> Vec2:
    # # #     """Returns size of this field calculated from `parent` canvas coords."""
    # # #     x0, y0, x1, y1 = self.parent.coords(self.id)
    # # #     return Vec2(x1, y1) - Vec2(x0, y0)
