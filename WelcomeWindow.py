import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk  # pip install pillow, import background image from og sketch
from HomeScreen import MainScreen

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

        # outer rectangle with semi opacity
        outer_margin = 35
        x0, y0 = outer_margin, outer_margin
        x1, y1 = 1330 - outer_margin, 750 - outer_margin
        canvas.create_rectangle(
            x0, y0, x1, y1,
            fill="white",
            stipple="gray50",
            outline="black",
            width=2,
        )

        # inner solid white rectangle
        inner_inset = 35
        canvas.create_rectangle(
            x0 + inner_inset, y0 + inner_inset,
            x1 - inner_inset, y1 - inner_inset,
            fill="white",
            outline="black",
            width=2,
        )

        # finding the center
        cx = 1330 // 2

        # title
        canvas.create_text(
	        cx, 260,
	        text="GameMatcher",
	        font=("Calisto MT", 120),
	        fill="black"
	    )
        
        # subtitle
        canvas.create_text(
	        cx, 370,
	        text="A Personalized Video Game Recommendation System",
	        font=("Calisto MT", 30),
	        fill="black"
        )

        # team members names
        canvas.create_text(
	        cx, 620,
	        text="Team Members: Iris Prifti, Alex Yan, Adiel Garcia",
	        font=("Calisto MT", 18),
	        fill="black"
        )

        # footer with team name
        canvas.create_text(
	        cx, 663,
	        text="Produced by Gamers Solutions",
	        font=("Calisto MT", 14, "bold"),
	        fill="black"
        )

        # start button
        btn = tk.Button(
	        self,
	        text="Click to Start",
	        font=("Calisto MT", 30, "bold"),
	        width=15,
	        relief="raised",
	        bd=4,
	        command=self.on_start
	    )
        canvas.create_window(cx, 500, window=btn)

    # when button is clicked, program closes welcome window and opens main screen
    def on_start(self):
        self.destroy()
        MainScreen().mainloop()
        
# starts running welcome window
if __name__ == "__main__":
    WelcomeScreen().mainloop()