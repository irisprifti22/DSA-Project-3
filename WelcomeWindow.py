import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow

class WelcomeScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher")
        self.geometry("1330x750")
        self.resizable(False, False)

if __name__ == "__main__":
    WelcomeScreen().mainloop()