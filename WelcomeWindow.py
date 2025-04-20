import tkinter as tk
from PIL import Image, ImageTk

class WelcomeScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher")
        self.geometry("800x400")
        self.resizable(False, False)

        # 1) load & resize the background image
        bg = Image.open("welcomeWindowBackground.jpg").resize((800, 400), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(bg)

        # 2) make a Canvas, put the image down
        self.canvas = tk.Canvas(self, width=800, height=400, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        # 3) draw a white rectangle with a stipple pattern (≈75% opacity)
        x0, y0, x1, y1 = 50, 50, 750, 350
        self.canvas.create_rectangle(
            x0, y0, x1, y1,
            fill="white",
            stipple="gray25",      # gray25 mask → about 75% fill
            outline="black",
            width=2
        )

        # 4) draw your title & subtitle
        self.canvas.create_text(
            400, 120,
            text="GameMatcher:",
            font=("Serif", 48, "bold"),
            fill="black"
        )
        self.canvas.create_text(
            400, 180,
            text="A Personalized Video Game Recommendation System",
            font=("Serif", 18),
            fill="black"
        )

        # 5) place a real Button on the canvas
        start_btn = tk.Button(
            self,
            text="Start Here!",
            font=("Serif", 16),
            width=15,
            command=self.on_start
        )
        self.canvas.create_window(400, 250, window=start_btn)

        # 6) footer text
        self.canvas.create_text(
            400, 330,
            text="Produced by Gamers Solutions",
            font=("Serif", 12),
            fill="black"
        )

    def on_start(self):
        self.destroy()
        MainApp()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher – Main")
        self.geometry("800x600")
        tk.Label(self, text="Main Application Window",
                 font=("Helvetica", 24)).pack(pady=50)
        self.mainloop()

if __name__ == "__main__":
    WelcomeScreen().mainloop()