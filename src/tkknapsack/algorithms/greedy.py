from tkknapsack.objects.node import Node


def greedy(capacity: float, nodeList: list[Node]) -> float:
    """
    :type capacity:float
    :type nodeList:list[node.Node]
    returns result of greedy algorithm as float
    """
    result = 0

    for node in nodeList:
        if node.weight <= capacity:
            capacity -= node.weight
            result += node.value

    return result
