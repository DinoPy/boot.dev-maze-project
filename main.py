from window import Window, Point, Cell, Maze


def main():
    w = Window(800, 800)
    maze = Maze(100, 100, 10, 10, 50, 50, w)
    maze._animate()

    w.wait_for_close()


if __name__ == "__main__":
    main()
