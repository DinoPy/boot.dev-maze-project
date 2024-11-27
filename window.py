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
        """ Will draw a line between the cell the function is called on
        and the given cell

        Parameters
        ----------
        to_cell : Cell
            The cell the line will be drawn to
        undo : Boolean
            boolean to enstablish undo eligibility
        """
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
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.num_rows):
            cols = []
            for j in range(self.num_cols):
                cols.append(
                    Cell(Point(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y),
                         Point(self.x1 + i * self.cell_size_x + self.cell_size_x,
                               self.y1 + j * self.cell_size_y + self.cell_size_y),
                         self.win)
                )
            self._cells.append(cols)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        """ Draws the cell at given coordinates

        Parameters
        ----------
        i : int
            The x coordinate of the cell to start at.
        j : int
            The y coordinate of the cell to start at.
        """
        self._cells[i][j].draw("red")
        self._animate()

    def _animate(self):
        """ Will call the window's redraw
        Will sleep for a given time
        """
        self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(self.num_rows-1, self.num_cols-1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while (True):
            to_visit = []
            # top
            if i > 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            # right
            if j < self.num_cols-1 and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))
            # bottom
            if i < self.num_rows-1 and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            # left
            if j > 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))

            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            random_dir_index = random.randrange(len(to_visit))
            next_index = to_visit[random_dir_index]

            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                # recursively visit the next cell
                self._cells[i][j - 1].has_bottom_wall = False
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False

    def solve(self):
        """ Invokes the recursive solve function at coordinates 0,0

        Returns
        ------
            True if the maze was solved successfully
        """
        return self._solve_r(0, 0)
        # return true if the maze was successfuly solved

    def _solve_r(self, i, j):
        """ Invokes the algorithm that will solve the maze.

        Parameters
        ----------
        i : int
            The x coordinate of the cell to start at.
        j : int
            The y coordinate of the cell to start at.
        """
        self._animate()
        self._cells[i][j].visited = True
        if i == self.num_rows-1 and j == self.num_cols-1:
            return True

         # move left if there is no wall and it hasn't been visited
        if (
            i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move right if there is no wall and it hasn't been visited
        if (
            i < self.num_rows - 1
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)

        # move up if there is no wall and it hasn't been visited
        if (
            j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        # move down if there is no wall and it hasn't been visited
        if (
            j < self.num_cols - 1
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # we went the wrong way let the previous cell know by returning False
        return False
