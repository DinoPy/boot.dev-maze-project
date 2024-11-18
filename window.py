from tkinter import Tk, BOTH, Canvas
import time


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.geometry(f"{height}x{width}")
        self.__root.title("Maze Runner")
        self.__canvas = Canvas(self.__root, height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__root.bind("<Key>", self.key_handler)
        self.is_window_running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.is_window_running = True
        while (self.is_window_running):
            self.redraw()

    def close(self):
        self.is_window_running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def key_handler(self, event):
        if event.char == " ":
            self.redraw()
            print("Key pressed", event.char)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )


class Cell:
    def __init__(self, p1, p2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = p1.x
        self._y1 = p1.y
        self._x2 = p2.x
        self._y2 = p2.y
        self._win = win

    def draw(self, win, color):
        xx = self._x2 - self._x1
        yy = self._y2 - self._y1
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x1 + xx, self._y1)
        p3 = Point(self._x2, self._y2)
        p4 = Point(self._x1, self._y1 + yy)
        if self.has_left_wall:
            left_wall = Line(p1, p4)
            self._win.draw_line(left_wall, color)
        if self.has_top_wall:
            top_wall = Line(p1, p2)
            self._win.draw_line(top_wall, color)
        if self.has_right_wall:
            right_wall = Line(p3, p2)
            self._win.draw_line(right_wall, color)
        if self.has_bottom_wall:
            bottom_wall = Line(p4, p3)
            self._win.draw_line(bottom_wall, color)

    def draw2(self, win, color):
        if self.has_top_wall:
            top_wall = Line(
                Point(self._x1, self._y1),
                Point(self._x2, self._y1))
            self._win.draw_line(top_wall, color)
        if self.has_top_wall:
            top_wall = Line(
                Point(self._x1, self._y2),
                Point(self._x2, self._y2))
            self._win.draw_line(top_wall, color)
        if self.has_right_wall:
            right_wall = Line(
                Point(self._x1, self._y2),
                Point(self._x1, self._y1))
            self._win.draw_line(right_wall, color)
        if self.has_left_wall:
            left_wall = Line(
                Point(self._x2, self._y2),
                Point(self._x2, self._y1))
            self._win.draw_line(left_wall, color)

    def draw_move(self, to_cell, undo=False):
        color = "red" if undo else "gray"
        x1, y1 = (abs(self._x1 + self._x2) / 2,
                  abs(self._y1 + self._y2) / 2)
        x2, y2 = (abs(to_cell._x1 + to_cell._x2) / 2,
                  abs(to_cell._y1 + to_cell._y2) / 2)
        line = Line(Point(x1, y1), Point(x2, y2))
        self._win.draw_line(line, color)


class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.matrix = []

        self._create_cells(self.x1, self.y1)

    def _create_cells(self, x, y):
        for i in range(self.num_rows):
            cols = []
            for j in range(self.num_cols):
                cols.append(
                    Cell(Point(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y),
                         Point(self.x1 + i * self.cell_size_x + self.cell_size_x,
                               self.y1 + j * self.cell_size_y + self.cell_size_y),
                         self.win)
                )
            self.matrix.append(cols)

    def _draw_cells(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                self.matrix[r][c].draw2(self.win, "red")

    def _animate(self):
        self._draw_cells()
        time.sleep(0.05)
