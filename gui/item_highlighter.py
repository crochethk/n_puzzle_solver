from tkinter import Canvas


class ItemHighlighter:
    def __init__(self, canvas: Canvas, item_id: int, color: str):
        self.canvas = canvas
        self.item_id = item_id
        self.color: str = color
        self.orig_color: str = ""

    def enable(self):
        self.orig_color = self.canvas.itemcget(self.item_id, "fill")
        self.canvas.itemconfigure(self.item_id, fill=self.color)

    def disable(self):
        self.canvas.itemconfigure(self.item_id, fill=self.orig_color)
