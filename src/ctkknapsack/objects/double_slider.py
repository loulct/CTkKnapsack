from customtkinter import CTk, CTkFrame, CTkLabel, CTkSlider, IntVar


class DoubleSlider(CTkFrame):
    def __init__(
        self,
        parent: CTk,
        label: str | None = None,
        min: int = 10,
        max: int = 100,
        row: int = 0,
        column: int = 0,
    ):
        super().__init__(parent)
        self.label = label
        self.min = IntVar(value=min)
        self.max = IntVar(value=max)

        self.grid(row=row, column=column + 1)

        self.label = CTkLabel(self, text=self._get_label())
        self.label.grid(row=row, column=column)

        self.slider_min = CTkSlider(
            self,
            from_=0,
            to=100,
            variable=self.min,
            command=self.update_min,
        )
        self.slider_min.grid(row=0, column=0)

        self.slider_max = CTkSlider(
            self,
            from_=0,
            to=100,
            variable=self.max,
            command=self.update_max,
        )
        self.slider_max.grid(row=1, column=0)

    def update_min(self, val):
        if int(val) >= self.max.get():
            self.slider_min.set(self.max.get() - 1)
        self.label.configure(text=self._get_label())

    def update_max(self, val):
        if int(val) <= self.min.get():
            self.slider_max.set(self.min.get() + 1)
        self.label.configure(text=self._get_label())

    def _get_label(self) -> str:
        return (
            f"{self.label} range: {self.min.get()} - {self.max.get()}"
            if self.label is not None
            else f"Range:  {self.min.get()} - {self.max.get()}"
        )
