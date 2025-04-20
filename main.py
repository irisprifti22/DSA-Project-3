import tkinter as tk

# main screen
class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher – Main")
        self.geometry("1330x750")
        tk.Label(self, text="Main Window",
                 font=("Calisto MT", 24)).pack(pady=50)

if __name__ == "__main__":
    # for testing
    MainScreen().mainloop()