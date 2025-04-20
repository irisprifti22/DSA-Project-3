import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk  # pip install pillow, import background image from og sketch
from Main import Main

# dimensions for base of welcome screen
class WelcomeScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher - Welcome")
        self.geometry("1330x750")
        self.resizable(False, False)

        # correct pathing for background image, makes it easier for team project
        base_dir = Path(__file__).resolve().parent
        img_path = base_dir / "resources" / "images" / "welcomeWindowBackground.jpg"

        bg = Image.open(img_path).resize((1330, 750), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(bg)

        # put it on canvas to finish background image
        canvas = tk.Canvas(self, width=1330, height=750, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

# starts running welcome window
if __name__ == "__main__":
    WelcomeScreen().mainloop()