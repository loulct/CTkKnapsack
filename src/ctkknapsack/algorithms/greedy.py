from ctkknapsack.objects.node import Node


def greedy(capacity: float, nodes: list[Node]) -> float:
    """
    :type capacity:float
    :type nodes:list[node.Node]
    returns result of greedy algorithm as float
    """
    result = 0

    for node in nodes:
        if node.weight <= capacity:
            capacity -= node.weight
            result += node.value

    return result
