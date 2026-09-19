from ctkknapsack.objects.node import Node


def not_greedy(capacity: float, nodes: list[Node]) -> tuple[float, list[Node], list]:
    """
    @type capacity:float
    @type nodes:list[node.Node]

    Returns a tuple with best value and path.
    """

    if len(nodes) > 9:
        return (0, [], [])

    switch_list = swap(nodes)
    temp = calculate_path(capacity, switch_list[0] if len(switch_list) > 0 else [])

    for path in switch_list:
        if calculate_path(capacity, path)[0] > temp[0]:
            temp = calculate_path(capacity, path)

    return temp


def swap(nodes: list[Node]) -> list[list[Node]]:
    """
    @type nodes:list[node.Node]

    Returns list of every possible swap outcome as switch_list:list[list[node.Node]].
    """
    switch_list = []

    if len(nodes) == 0:
        return []

    if len(nodes) == 1:
        switch_list = [nodes]
    else:
        for index in range(len(nodes)):
            permutation = swap(nodes[0:index] + nodes[index + 1 : len(nodes)])
            for node in permutation:
                switch_list.append([nodes[index]] + node)

    return switch_list


def calculate_path(
    capacity: float, nodes: list[Node]
) -> tuple[float, list[Node], list]:
    """
    @type nodes:list[node.Node]

    Returns a tuple[value:float | Literal[0], nodes:list[node.Node], path:list]
    """
    result = (0, [], [])
    value = 0
    path = []

    for node in nodes:
        if node.weight < capacity:
            capacity -= node.weight
            value += node.value
            path.append(1)
        else:
            path.append(0)

    result = (value, nodes, path)
    return result
