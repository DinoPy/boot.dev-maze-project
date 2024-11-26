from window import Window, Maze


def main():
    w = Window(1000, 1000)
    maze = Maze(50, 50, 12, 16, 50, 50, w)
    maze.test()

    w.wait_for_close()


if __name__ == "__main__":
    main()
