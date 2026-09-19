from tkinter.ttk import Style

from ctkknapsack.style.hexcode import HexCode


class TreeviewStyle(Style):
    def __init__(self):
        super().__init__()

        self.theme_use("clam")

        self.configure(
            "Treeview",
            background=HexCode.BG,
            foreground=HexCode.TEXT,
            fieldbackground=HexCode.BG,
            rowheight=35,
            font=("Segoe UI", 10),
            borderwidth=0,
        )

        self.map(
            "Treeview",
            background=[("selected", HexCode.SELECTED)],
            foreground=[("selected", "#ffffff")],
        )

        self.configure(
            "Treeview.Heading",
            background=HexCode.HEADER,
            foreground=HexCode.TEXT,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            relief="flat",
        )

        self.map(
            "Treeview.Heading",
            background=[("active", HexCode.HEADER)],
            foreground=[("active", HexCode.TEXT)],
        )
