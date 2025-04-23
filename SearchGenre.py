import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk
from red_black_tree import RBTree

class SearchGenreScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GameMatcher – Search by Genre")
        self.geometry("1330x750")
        self.resizable(False, False)

        # background image
        base_dir = Path(__file__).resolve().parent
        img_path = base_dir / "resources" / "images" / "welcomeWindowBackground.jpg"
        bg = Image.open(img_path).resize((1330, 750), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(bg)
        canvas = tk.Canvas(self, width=1330, height=750, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        # outer white frame
        pad_x, pad_y = 50, 50
        canvas.create_rectangle(
            pad_x, pad_y,
            1330 - pad_x, 750 - pad_y,
            fill="white",
            outline="black",
            width=2
        )

        # banner for entry
        banner = tk.Frame(self, bg="#EEEEEE", bd=1, relief="solid")
        canvas.create_window(665, 120, window=banner, width=1100, height=60)

        lbl = tk.Label(banner,
                       text="Enter a Genre:",
                       font=("Calisto MT", 18),
                       bg="#EEEEEE")
        lbl.pack(side="left", padx=(5,5))

        self.search_entry = tk.Entry(banner,
                                     font=("Calisto MT", 18),
                                     width=100)
        self.search_entry.pack(side="left", padx=(0,10))

        # Search / Clear buttons
        btn_cfg = {"font":("Calisto MT", 18), "width":12}
        btn_search = tk.Button(self, text="Search",
                               command=self.perform_search,
                               **btn_cfg)
        btn_clear  = tk.Button(self, text="Clear",
                               command=self.clear_results,
                               **btn_cfg)
        canvas.create_window(600, 200, window=btn_search)
        canvas.create_window(760, 200, window=btn_clear)

        # results area
        results_frame = tk.LabelFrame(self,
            text="Results",
            bg="#DDDDDD", fg="black",
            font=("Calisto MT", 16, "bold"),
            labelanchor="n",
            bd=2, relief="raised",
            padx=5, pady=5
        )
        canvas.create_window(665, 450,
                             window=results_frame,
                             width=1200, height=350)

        # tree columns
        cols = ("#", "Title", "Genres", "Developers", "Platforms")
        self.tree = ttk.Treeview(results_frame,
                                 columns=cols,
                                 show="headings",
                                 height=10)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Calisto MT", 14))
        style.configure("Treeview", font=("Calisto MT", 12))
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col,
                             anchor="w",
                             width=200 if col!="#" else 30)

        vsb = ttk.Scrollbar(results_frame,
                            orient="vertical",
                            command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        # data manager
        self.manager = RBTree()
        self.manager.read()

    def perform_search(self):
        genre = self.search_entry.get().strip()
        recs  = self.manager.get_recommendations_by_genre(genre)

        # clear old results
        for iid in self.tree.get_children():
            self.tree.delete(iid)

        # show error or insert rows
        if recs and recs[0][0] == 'ERRORNULL':
            self.tree.insert("", "end",
                values=( "", f"No games found in genre “{genre}”", "", "", "" )
            )
            return

        for i, (title, genres, devs, plats) in enumerate(recs, start=1):
            self.tree.insert("", "end",
                values=(i,
                        title,
                        ", ".join(genres),
                        ", ".join(devs),
                        ", ".join(plats))
            )

    def clear_results(self):
        self.search_entry.delete(0, tk.END)
        for iid in self.tree.get_children():
            self.tree.delete(iid)

if __name__ == "__main__":
    SearchGenreScreen().mainloop()