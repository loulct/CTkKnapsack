import math
from random import uniform
from tkinter import *

try:
    import operator
except ImportError:
    sortkey = lambda x: x.value_per_weight
else:
    sortkey = operator.attrgetter("value_per_weight")

from algorithms.greedy import greedy
from algorithms.not_greedy import not_greedy
from objects.node import Node


class Interface(Frame):
    def __init__(self, window, **kwargs):
        Frame.__init__(self, window, **kwargs)

        self.final_value = 0
        self.list = []

        global capacity, number_of_nodes, min_weight, max_weight, min_value, max_value

        # Display final value
        self.label = Label(window, text="Input values")
        self.label.grid(row=1, column=2)
        self.label2 = Label(window, text="")
        self.label2.grid(row=2, column=2)

        # Quit button (uses .destroy)
        window.quit = Button(window, text="Quit", command=window.destroy)
        window.quit.grid(row=1, column=1)

        self.display = Label(window, text="Capacity : ")
        self.display.grid(row=3, column=1)
        capacity = Entry(window, width=10)
        capacity.insert(0, "100")
        capacity.grid(row=3, column=2)

        self.display = Label(window, text="Number of nodes : ")
        self.display.grid(row=4, column=1)
        number_of_nodes = Entry(window, width=10)
        number_of_nodes.insert(0, "5")
        number_of_nodes.grid(row=4, column=2)

        self.display = Label(window, text="Minimum weight of nodes : ")
        self.display.grid(row=5, column=1)
        min_weight = Entry(window, width=10)
        min_weight.insert(0, "10")
        min_weight.grid(row=5, column=2)

        self.display = Label(window, text="Maximum weight of nodes : ")
        self.display.grid(row=6, column=1)
        max_weight = Entry(window, width=10)
        max_weight.insert(0, "100")
        max_weight.grid(row=6, column=2)

        self.display = Label(window, text="Minimum value of nodes : ")
        self.display.grid(row=7, column=1)
        min_value = Entry(window, width=10)
        min_value.insert(0, "10")
        min_value.grid(row=7, column=2)

        self.display = Label(window, text="Maximum value of nodes : ")
        self.display.grid(row=8, column=1)
        max_value = Entry(window, width=10)
        max_value.insert(0, "100")
        max_value.grid(row=8, column=2)

        self.create_nodes = Button(
            window, text="Create nodes", command=self.generateNode
        )
        self.create_nodes.grid(row=9, column=1)
        self.launch_greedy = Button(
            window, text="Greedy Algorithm", command=self.launchGreedy
        )
        self.launch_greedy.grid(row=9, column=2)
        self.launch_not_greedy = Button(
            window, text="Not Greedy Algorithm", command=self.launchNotGreedy
        )
        self.launch_not_greedy.grid(row=9, column=3)

        self.large = 400
        self.height = 400
        self.angle = math.pi / 5  # angle between two branches
        self.taille = 0.58  # height of branches

        self.canvas = Canvas(window, width=self.large, height=self.height, bg="white")
        self.canvas.grid(row=1, rowspan=11, column=4)

        self.display = Label(window, text="Value")
        self.display.grid(row=10, column=1)
        self.display = Label(window, text="Weight")
        self.display.grid(row=10, column=2)
        self.display = Label(window, text="Value per weight")
        self.display.grid(row=10, column=3)

        self.scrollbar = Scrollbar(window)
        self.scrollbar.grid(row=11, column=4, sticky=W + N + S)

        self.listbox = Listbox(window, width=60, yscrollcommand=self.scrollbar.set)
        self.listbox.grid(row=11, column=1, columnspan=3)

    def launchGreedy(self) -> None:
        """ """
        self.final_value = greedy(
            float(capacity.get()), sorted(self.list, key=sortkey, reverse=True)
        )
        self.label["text"] = f"Final value : {self.final_value}"

    def launchNotGreedy(self) -> None:
        """ """
        self.final_value = not_greedy(float(capacity.get()), self.list)
        self.path = self.final_value[2]
        self.label2["text"] = f"Final value : {self.final_value[0]}"

        self.canvas.delete("line")
        depth = len(self.list)

        self.drawBranch(
            depth,
            self.large / 2,
            self.height,
            self.height / 3,
            math.pi / 2,
            color="black",
        )
        self.drawPath(depth, self.large / 2, self.height, self.height / 3, math.pi / 2)

        rang = len(self.final_value[1])
        for node in self.final_value[1]:
            self.listbox.insert(
                END,
                str(node.value)
                + " | "
                + str(node.weight)
                + " | "
                + str(node.value_per_weight)
                + " | "
                + str(rang),
            )
            self.listbox.grid(row=11, column=1, columnspan=3)
            self.scrollbar.config(command=self.listbox.yview)
            rang -= 1

    def generateNode(self) -> None:
        """ """
        nodeList = []

        for index in range(int(number_of_nodes.get())):
            unique_node = Node(
                uniform(float(min_weight.get()), float(max_weight.get())),
                uniform(float(min_value.get()), float(max_value.get())),
            )
            nodeList.append(unique_node)

        self.list = sorted(nodeList, key=sortkey, reverse=True)

        self.listbox.delete(0, "end")
        for node in self.list:
            self.listbox.insert(
                END,
                str(node.value)
                + " | "
                + str(node.weight)
                + " | "
                + str(node.value_per_weight),
            )
            self.listbox.grid(row=11, column=1, columnspan=3)
            self.scrollbar.config(command=self.listbox.yview)

    def drawLine(self, x1: float, y1: float, x2: int, y2: int, color: str) -> None:
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
            x2 = x1 + int(math.cos(angle) * length)
            y2 = y1 - int(math.sin(angle) * length)

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
            x2 = x1 + int(math.cos(angle) * length)
            y2 = y1 - int(math.sin(angle) * length)

            self.drawLine(x1, y1, x2, y2, "blue")
            if self.path[depth] == 1:
                self.drawPath(depth, x2, y2, length * self.taille, angle + self.angle)
            else:
                self.drawPath(depth, x2, y2, length * self.taille, angle - self.angle)
