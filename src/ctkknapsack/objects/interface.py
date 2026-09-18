from math import cos, pi, sin
from random import uniform
from tkinter.ttk import Style, Treeview

from customtkinter import (
    CTk,
    CTkButton,
    CTkCanvas,
    CTkFrame,
    CTkLabel,
    CTkScrollbar,
    CTkSlider,
    IntVar,
)

from ctkknapsack.objects.spinbox import CustomSpinbox

try:
    import operator
except ImportError:
    sortkey = lambda x: x.ratio
else:
    sortkey = operator.attrgetter("ratio")

from ctkknapsack.algorithms.greedy import greedy
from ctkknapsack.algorithms.not_greedy import not_greedy
from ctkknapsack.objects.node import Node


class Interface(CTk):
    def __init__(self, **kwargs):
        super().__init__()
        self.geometry("1250x600")
        self.resizable(False, False)
        self.title("Knapsack Problem")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        style = Style()
        style.theme_use("clam")

        bg_color = "#2b2b2b"
        text_color = "#ffffff"
        selected_color = "#1f6aa5"
        header_bg = "#343638"

        style.configure(
            "Treeview",
            background=bg_color,
            foreground=text_color,
            fieldbackground=bg_color,
            rowheight=35,
            font=("Segoe UI", 10),
            borderwidth=0,
        )

        style.map(
            "Treeview",
            background=[("selected", selected_color)],
            foreground=[("selected", "#ffffff")],
        )

        style.configure(
            "Treeview.Heading",
            background=header_bg,
            foreground=text_color,
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            relief="flat",
        )

        style.map(
            "Treeview.Heading",
            background=[("active", header_bg)],
            foreground=[("active", text_color)],
        )

        self.final_value = 0
        self.list = []

        result_container = CTkFrame(self)
        result_container.grid(row=2, column=5)
        self.result_label = CTkLabel(result_container, text="Result: ")
        self.result_label.grid(row=0, column=0)
        self.result = CTkLabel(result_container, text="")
        self.result.grid(row=0, column=1)

        CTkLabel(self, text="Capacity").grid(row=2, column=1)
        self.capacity = CustomSpinbox(self, width=200)
        self.capacity.set(100)
        self.capacity.grid(row=2, column=2)

        CTkLabel(self, text="Node count").grid(row=3, column=1)
        self.nodes = CustomSpinbox(self, width=200)
        self.nodes.set(5)
        self.nodes.grid(row=3, column=2)

        self.min_weight = IntVar(value=10)
        self.max_weight = IntVar(value=100)

        slider_container = CTkFrame(self)
        slider_container.grid(row=4, column=2)
        self.weight_label = CTkLabel(
            self,
            text=f"Weight range: {self.min_weight.get()} - {self.max_weight.get()}",
        )
        self.weight_label.grid(row=4, column=1)

        self.weight_slider_min = CTkSlider(
            slider_container,
            from_=0,
            to=100,
            variable=self.min_weight,
            command=self.update_min_weight,
        )
        self.weight_slider_min.grid(row=0, column=0)
        self.weight_slider_max = CTkSlider(
            slider_container,
            from_=0,
            to=100,
            variable=self.max_weight,
            command=self.update_max_weight,
        )
        self.weight_slider_max.grid(row=1, column=0)

        self.min_value = IntVar(value=10)
        self.max_value = IntVar(value=100)

        slider_container = CTkFrame(self)
        slider_container.grid(row=5, column=2)
        self.value_label = CTkLabel(
            self, text=f"Value range: {self.min_value.get()} - {self.max_value.get()}"
        )
        self.value_label.grid(row=5, column=1)

        self.value_slider_min = CTkSlider(
            slider_container,
            from_=0,
            to=100,
            variable=self.min_value,
            command=self.update_min_value,
        )
        self.value_slider_min.grid(row=0, column=0)
        self.value_slider_max = CTkSlider(
            slider_container,
            from_=0,
            to=100,
            variable=self.max_value,
            command=self.update_max_value,
        )
        self.value_slider_max.grid(row=1, column=0)

        self.create_nodes = CTkButton(
            self, text="Create nodes", command=self.generateNode
        )
        self.create_nodes.grid(row=8, column=1)
        self.launch_greedy = CTkButton(
            self, text="Greedy Algorithm", command=self.launchGreedy
        )
        self.launch_greedy.grid(row=8, column=2)
        self.launch_not_greedy = CTkButton(
            self, text="Not Greedy Algorithm", command=self.launchNotGreedy
        )
        self.launch_not_greedy.grid(row=8, column=3)

        self.large = 400
        self.height = 450
        self.angle = pi / 5  # angle between two branches
        self.taille = 0.58  # height of branches

        self.canvas = CTkCanvas(self, width=self.large, height=self.height, bg="white")
        self.canvas.grid(row=1, rowspan=11, column=5)

        self.columns = ("Value", "Weight", "Ratio", "Rank")
        self.table = Treeview(self, columns=self.columns, show="headings")
        self.table.heading("Value", text="Value")
        self.table.heading("Weight", text="Weight")
        self.table.heading("Ratio", text="Ratio")
        self.table.heading("Rank", text="Rank")

        self.scrollbar = CTkScrollbar(
            self, orientation="vertical", command=self.table.yview
        )

        self.table.configure(yscrollcommand=self.scrollbar.set)

        self.table.grid(row=11, column=1, columnspan=3)
        self.scrollbar.grid(row=11, column=4, sticky="wns")

    def on_closing(self):
        self.quit()
        self.destroy()

    def update_min_value(self, val):
        if int(val) >= self.max_value.get():
            self.value_slider_min.set(self.max_value.get() - 1)
        self.value_label.configure(
            text=f"Value range: {self.min_value.get()} - {self.max_value.get()}"
        )

    def update_max_value(self, val):
        if int(val) <= self.min_value.get():
            self.value_slider_max.set(self.min_value.get() + 1)
        self.value_label.configure(
            text=f"Value range: {self.min_value.get()} - {self.max_value.get()}"
        )

    def update_min_weight(self, val):
        if int(val) >= self.max_weight.get():
            self.weight_slider_min.set(self.max_weight.get() - 1)
        self.weight_label.configure(
            text=f"Weight range: {self.min_weight.get()} - {self.max_weight.get()}"
        )

    def update_max_weight(self, val):
        if int(val) <= self.min_weight.get():
            self.weight_slider_max.set(self.min_weight.get() + 1)
        self.weight_label.configure(
            text=f"Weight range: {self.min_weight.get()} - {self.max_weight.get()}"
        )

    def launchGreedy(self) -> None:
        """ """
        self.final_value = greedy(
            float(self.capacity.get()), sorted(self.list, key=sortkey, reverse=True)
        )
        self.result.configure(text=self.final_value)

    def launchNotGreedy(self) -> None:
        """ """
        self.final_value = not_greedy(float(self.capacity.get()), self.list)
        self.path = self.final_value[2]
        self.result.configure(text=self.final_value[0])

        self.canvas.delete("all")
        depth = len(self.list)

        self.drawBranch(
            depth,
            self.large / 2,
            self.height,
            self.height / 3,
            pi / 2,
            color="black",
        )
        self.drawPath(depth, self.large / 2, self.height, self.height / 3, pi / 2)

        rang = len(self.final_value[1])
        self.clear_table()
        for node in self.final_value[1]:
            self.table.insert(
                "", "end", values=(node.value, node.weight, node.ratio, rang)
            )
            rang -= 1

    def generateNode(self) -> None:
        """ """
        self.canvas.delete("all")
        nodeList = []

        for index in range(int(self.nodes.get())):
            unique_node = Node(
                uniform(float(self.min_weight.get()), float(self.max_weight.get())),
                uniform(float(self.min_value.get()), float(self.max_value.get())),
            )
            nodeList.append(unique_node)

        self.list = sorted(nodeList, key=sortkey, reverse=True)

        self.clear_table()
        for node in self.list:
            self.table.insert("", "end", values=(node.value, node.weight, node.ratio))

    def clear_table(self):
        if self.table.get_children():
            for item in self.table.get_children():
                self.table.delete(item)

    def drawLine(self, x1: float, y1: float, x2: float, y2: float, color: str) -> None:
        """
        @type x1:float
        @type y1:float
        @type x2:int
        @type y2:int
        @type color:string
        """
        self.canvas.create_line(x1, y1, x2, y2, fill=color, tags="line")

    def drawBranch(
        self, depth: int, x1: float, y1: float, length: float, angle: float, color: str
    ) -> None:
        """
        @type depth:int
        @type x1:float
        @type y1:float
        @type length:float
        @type angle:float
        @type color:string
        """
        if depth >= 0:
            depth -= 1
            x2 = x1 + int(cos(angle) * length)
            y2 = y1 - int(sin(angle) * length)

            self.drawLine(x1, y1, x2, y2, color)

            if self.path[depth] == 1:
                self.drawBranch(
                    depth,
                    x2,
                    y2,
                    length * self.taille,
                    angle + self.angle,
                    color="green",
                )
                self.drawBranch(
                    depth, x2, y2, length * self.taille, angle - self.angle, color="red"
                )
            else:
                self.drawBranch(
                    depth,
                    x2,
                    y2,
                    length * self.taille,
                    angle + self.angle,
                    color="green",
                )
                self.drawBranch(
                    depth, x2, y2, length * self.taille, angle - self.angle, color="red"
                )

            if depth != len(self.list) - 1:
                self.canvas.create_text(
                    x2, y2, text=(len(self.list) - depth - 1), fill="black"
                )

    def drawPath(
        self, depth: int, x1: float, y1: float, length: float, angle: float
    ) -> None:
        """
        @type depth:int
        @type x1:float
        @type y1:float
        @type length:float
        @type angle:float
        """
        if depth >= 0:
            depth -= 1
            x2 = x1 + int(cos(angle) * length)
            y2 = y1 - int(sin(angle) * length)

            self.drawLine(x1, y1, x2, y2, "blue")
            if self.path[depth] == 1:
                self.drawPath(depth, x2, y2, length * self.taille, angle + self.angle)
            else:
                self.drawPath(depth, x2, y2, length * self.taille, angle - self.angle)
