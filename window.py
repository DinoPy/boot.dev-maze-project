from tkinter import Tk, BOTH, Canvas
from enum import Enum
import random
import time


class Directions(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Runner")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
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
        self.visited = False

    def __repr__(self):
        return f"Walls: Top: {self.has_top_wall}, Bottom: {self.has_bottom_wall}, Right: {self.has_right_wall}, Left: {self.has_left_wall}. " + \
            f"x1: {self._x1}, y1: {self._y1}, x2: {self._x2}, y2: {self._y2}"

    def draw(self, color):
        if self.has_top_wall:
            top_wall = Line(
                Point(self._x1, self._y1),
                Point(self._x2, self._y1))
            self._win.draw_line(top_wall, color)
        else:
            top_wall = Line(
                Point(self._x1, self._y1),
                Point(self._x2, self._y1))
            self._win.draw_line(top_wall, "white")

        if self.has_bottom_wall:
            bottom_wall = Line(
                Point(self._x1, self._y2),
                Point(self._x2, self._y2))
            self._win.draw_line(bottom_wall, color)
        else:
            bottom_wall = Line(
                Point(self._x1, self._y2),
                Point(self._x2, self._y2))
            self._win.draw_line(bottom_wall, "white")

        if self.has_right_wall:
            right_wall = Line(
                Point(self._x2, self._y1),
                Point(self._x2, self._y2))
            self._win.draw_line(right_wall, color)
        else:
            right_wall = Line(
                Point(self._x2, self._y1),
                Point(self._x2, self._y2))
            self._win.draw_line(right_wall, "white")
        if self.has_left_wall:
            left_wall = Line(
                Point(self._x1, self._y1),
                Point(self._x1, self._y2))
            self._win.draw_line(left_wall, color)
        else:
            left_wall = Line(
                Point(self._x1, self._y1),
                Point(self._x1, self._y2))
            self._win.draw_line(left_wall, "white")

    def draw_move(self, to_cell, undo=False):
        color = "red" if undo else "gray"
        x1, y1 = (abs(self._x1 + self._x2) // 2,
                  abs(self._y1 + self._y2) // 2)
        x2, y2 = (abs(to_cell._x1 + to_cell._x2) // 2,
                  abs(to_cell._y1 + to_cell._y2) // 2)
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
            seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = random.seed(seed) if seed else None
        self._cells = []

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r_2(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.num_cols):
            cols = []
            for j in range(self.num_rows):
                cols.append(
                    Cell(Point(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y),
                         Point(self.x1 + i * self.cell_size_x + self.cell_size_x,
                               self.y1 + j * self.cell_size_y + self.cell_size_y),
                         self.win)
                )
            self._cells.append(cols)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw("red")
        self._animate()

    '''
        Will call the window's redraw
        Will sleep for a given time
    '''
    def _animate(self):
        self.win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self.num_cols-1, self.num_rows-1)

    def test(self):
        for i in range(self.num_cols):
            print("----- NEW ROW -----")
            for j in range(self.num_rows):
                print(f"{i} - {j}", self._cells[i][j], "\n")

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while (True):
            to_visit = []
            # top
            if i-1 >= 0 and not self._cells[i-1][j].visited:
                to_visit.append((Directions.TOP, self._cells[i-1][j]))
            # right
            if j+1 <= self.num_rows-1 and not self._cells[i][j+1].visited:
                to_visit.append((Directions.RIGHT, self._cells[i][j+1]))
            # bottom
            if i+1 <= self.num_cols-1 and not self._cells[i+1][j].visited:
                to_visit.append((Directions.BOTTOM, self._cells[i+1][j]))
            # left
            if j-1 >= 0 and not self._cells[i][j-1].visited:
                to_visit.append((Directions.LEFT, self._cells[i][j-1]))

            if len(to_visit) < 1:
                self._cells[i][j].draw("red")
                return

            rand = random.randrange(len(to_visit))
            m, n = 0, 0

            if to_visit[rand][0] == Directions.TOP:
                self._cells[i][j].has_top_wall = False
                to_visit[rand][1].has_bottom_wall = False
                m, n = i-1, j
            elif to_visit[rand][0] == Directions.RIGHT:
                self._cells[i][j].has_right_wall = False
                to_visit[rand][1].has_left_wall = False
                m, n = i, j+1
            elif to_visit[rand][0] == Directions.BOTTOM:
                self._cells[i][j].has_bottom_wall = False
                to_visit[rand][1].has_top_wall = False
                m, n = i+1, j
            elif to_visit[rand][0] == Directions.LEFT:
                self._cells[i][j].has_left_wall = False
                to_visit[rand][1].has_right_wall = False
                m, n = i, j-1

            self._draw_cell(m, n)
            self._break_walls_r(m, n)

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)
        # return true if the maze was successfuly solved

    def _solve_r(self, i, j):
        self._animate()
