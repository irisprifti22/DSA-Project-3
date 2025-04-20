import tkinter as tk
from PIL import Image, ImageTk  # pip install pillow, import background image from og sketch
from main import Main

# dimensions for base of welcome screen
class WelcomeScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher - Welcome")
        self.geometry("1330x750")
        self.resizable(False, False)

# starts running welcome window
if __name__ == "__main__":
    WelcomeScreen().mainloop()