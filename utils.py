import tsplib95
import math
import numpy as np

def load_from_tsp(path):
    problem = tsplib95.load(path)
    coords = problem.node_coords
    n = problem.dimension
    distance_matrix = np.zeros((n, n), dtype=int)

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                distance_matrix[i - 1, j - 1] = 0
            else:
                x1, y1 = coords[i]
                x2, y2 = coords[j]
                distance = math.hypot(x1 - x2, y1 - y2)
                distance_matrix[i - 1, j - 1] = round(distance)

    return distance_matrix

def experiment(matrix, algorithm, runs=100):
    total_costs = []
    min_cost = float('inf')
    max_cost = float('-inf')

    for i in range(runs):
        cycle1, cycle2 = algorithm(matrix)
        length1 = cycle_length(cycle1, matrix)
        length2 = cycle_length(cycle2, matrix)
        total = length1 + length2
        total_costs.append(total)

        if total < min_cost:
            min_cost = total
        if total > max_cost:
            max_cost = total

    avg_cost = sum(total_costs) / runs
    return avg_cost, min_cost, max_cost

def run_test(algorithm_name: str, distance_matrix: np.ndarray, algorithm):
    avg_alg, min_alg, max_alg = experiment(distance_matrix, algorithm)
    print(f"{algorithm_name} - Średnia: {avg_alg:.2f}, Min: {min_alg}, Max: {max_alg}")

def cycle_length(cycle, matrix):
    length = 0
    for i in range(1, len(cycle)):
        length += matrix[cycle[i - 1]][cycle[i]]
    return length

def initialize_cycles(distance_matrix: np.ndarray) -> tuple[list[int], list[int], set[int]]:
    n = len(distance_matrix)
    nodes = set(range(n))
    
    first_node = np.random.choice(list(nodes))
    nodes.remove(first_node)
    
    second_node = min(nodes, key=lambda x: distance_matrix[first_node][x])
    nodes.remove(second_node)
    
    cycle1 = [first_node]
    cycle2 = [second_node]
    
    return cycle1, cycle2, nodes

def calculate_regret(distance_matrix: np.ndarray, cycle: list[int], candidate: int) -> tuple[float, float, int]:
    best_increase = float('inf')
    second_best_increase = float('inf')
    best_pos = -1
    
    for i in range(len(cycle)):
        j = (i + 1) % len(cycle)
        increase = (
            distance_matrix[cycle[i]][candidate] +
            distance_matrix[candidate][cycle[j]] -
            distance_matrix[cycle[i]][cycle[j]]
        )
        
        if increase < best_increase:
            second_best_increase = best_increase
            best_increase = increase
            best_pos = j
        elif increase < second_best_increase:
            second_best_increase = increase
    
    regret = second_best_increase - best_increase
    return regret, best_increase, best_pos

def insert_into_cycle(distance_matrix: np.ndarray, cycle: list[int], candidate: int) -> None:
    _, _, pos = calculate_regret(distance_matrix, cycle, candidate)
    cycle.insert(pos, candidate)