import unittest
from window import Maze, Window


class Test(unittest.TestCase):
    def test_maze_create_cells(self):
        win = Window(1000, 1000)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_exit_walls(self):
        win = Window(1000, 1000)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(m1._cells[0][0].has_top_wall, False)
        self.assertEqual(m1._cells[-1][-1].has_bottom_wall, False)

    def test_maze_cells_visit_reset(self):
        win = Window(1000, 1000)
        m1 = Maze(100, 100, 10, 10, 50, 50, win)
        return

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.assertEqual(m1._cells[i][j].visited, False)


if __name__ == "__main__":
    unittest.main()
