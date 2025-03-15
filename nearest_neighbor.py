import random
import numpy as np

def nearest_neighbor(matrix):
    n = len(matrix)
    nodes = list(range(n))

    start_point1 = random.choice(nodes)
    start_point2 = int(np.argmax(matrix[start_point1]))

    remaining_nodes = set(nodes) - {start_point1, start_point2}

    first_cycle = [start_point1]
    second_cycle = [start_point2]

    vertices_num = (n + 1) // 2
    vertices_num2 = n // 2

    while len(first_cycle) < vertices_num:
        last = first_cycle[-1]
        nearest = min(remaining_nodes, key=lambda node: matrix[last][node])
        first_cycle.append(nearest)
        remaining_nodes.remove(nearest)

    while len(second_cycle) < vertices_num2:
        last = second_cycle[-1]
        nearest = min(remaining_nodes, key=lambda node: matrix[last][node])
        second_cycle.append(nearest)
        remaining_nodes.remove(nearest)

    first_cycle.append(start_point1)
    second_cycle.append(start_point2)


    return first_cycle, second_cycle