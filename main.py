import tkinter as tk

# main screen
class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher – Main Screen")
        self.geometry("1330x750")
        self.resizable(False, False)

if __name__ == "__main__":
    # for testing
    Main().mainloop()
