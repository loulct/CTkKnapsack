from ctkknapsack.objects.node import Node


def not_greedy(capacity: float, nodeList: list[Node]) -> tuple[float, list[Node], list]:
    """
    @type capacity:float
    @type nodeList:list[node.Node]

    Returns a tuple with best value and path.
    """

    if len(nodeList) > 9:
        return (0, [], [])

    switchList = swap(nodeList)
    temp = calculatePath(capacity, switchList[0] if len(switchList) > 0 else [])

    for path in switchList:
        if calculatePath(capacity, path)[0] > temp[0]:
            temp = calculatePath(capacity, path)

    return temp


def swap(nodeList: list[Node]) -> list[list[Node]]:
    """
    @type nodeList:list[node.Node]

    Returns list of every possible swap outcome as switchList:list[list[node.Node]] or None.
    """
    switchList = []

    if len(nodeList) == 0:
        return []

    if len(nodeList) == 1:
        switchList = [nodeList]
    else:
        for index in range(len(nodeList)):
            permutation = swap(nodeList[0:index] + nodeList[index + 1 : len(nodeList)])
            for node in permutation:
                switchList.append([nodeList[index]] + node)

    return switchList


def calculatePath(
    capacity: float, nodeList: list[Node]
) -> tuple[float, list[Node], list]:
    """
    @type nodeList:list[node.Node]

    Returns a tuple[value:float | Literal[0], nodeList:list[node.Node], path:list]
    """
    result = (0, [], [])
    value = 0
    path = []

    for node in nodeList:
        if node.weight < capacity:
            capacity -= node.weight
            value += node.value
            path.append(1)
        else:
            path.append(0)

    result = (value, nodeList, path)
    return result
