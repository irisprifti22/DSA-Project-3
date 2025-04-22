import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from SearchName import SearchNameScreen
from SearchGenre import SearchGenreScreen

# main screen
class MainScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher – Home Screen")
        self.geometry("1330x750")
        self.resizable(False, False)

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
	        cx, 220,
	        text="Welcome to GameMatcher!",
	        font=("Calisto MT", 67),
	        fill="black"
	    )

        # subtitle
        canvas.create_text(
	        cx, 320,
	        text="Feeling lost in a sea of game titles? Tired of endless browsing? Just enter the name of your favorite",
	        font=("Calisto MT", 18),
	        fill="black"
        )
        canvas.create_text(
	        cx, 355,
            text="game or your favorite genre, and our smart engine will find the right games that match your taste.",
	        font=("Calisto MT", 18),
	        fill="black"
        )
        canvas.create_text(
	        cx, 390,
            text="We deliver fast and personalized suggestions so you can jump straight into fun!",
	        font=("Calisto MT", 18),
	        fill="black"
        )
        canvas.create_text(
	        cx, 480,
            text="Please select how you will be searching today:",
	        font=("Calisto MT", 20, "bold"),
	        fill="black"
        )
        # footer with team name
        canvas.create_text(
	        cx, 663,
	        text="Produced by Gamers Solutions",
	        font=("Calisto MT", 14, "bold"),
	        fill="black"
        )

        # buttons for separate search screens
        btn_cfg = {
            "font": ("Calisto MT", 20, "bold"),
            "width": 15,
            "bd": 4,
            "relief": "raised",
        }

        # name search button
        btn_name = tk.Button(self, text="Search by Title", command=self.open_search_name, **btn_cfg)
        # genre search button
        btn_genre = tk.Button(self, text="Search by Genre", command=self.open_search_genre, **btn_cfg)

        # places buttons on the canvas
        canvas.create_window(cx - 200, 560, window=btn_name)
        canvas.create_window(cx + 200, 560, window=btn_genre)

    # closes HomeScreen and opens SearchNameScreen
    def open_search_name(self):
        self.destroy()
        SearchNameScreen().mainloop()

    # closes HomeScreen and opens SearchGenreScreen
    def open_search_genre(self):
        self.destroy()
        SearchGenreScreen().mainloop()

if __name__ == "__main__":
    # for testing
    MainScreen().mainloop()