class Node:
    def __init__(self, weight: float, value: float) -> None:
        """
        @type weight:float
        @type value:float
        """

        self.weight = weight
        self.value = value
        self.ratio = value / weight
