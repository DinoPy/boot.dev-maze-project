from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.geometry(f"{height}x{width}")
        self.__root.title("Maze Runner")
        self.__canvas = Canvas(self.__root, height=height, width=width)
        self.__canvas.pack()
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

