class Node:
    def __init__(self, weight: float, value: float):
        """
        @type weight:float
        @type value:float
        """

        self.weight = weight
        self.value = value
        self.value_per_weight = value / weight
