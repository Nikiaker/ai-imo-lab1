import tsplib95
import math
import numpy as np
import matplotlib.pyplot as plt

from typing import Callable

def convert_tsp_to_array(tsp_coords: tsplib95.fields.IndexedCoordinatesField, size: int) -> np.ndarray:
    list_coords = []
    for i in range(1, size + 1):
        list_coords.append(tsp_coords[i])
    return np.array(list_coords)

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

    coords_matrix = convert_tsp_to_array(coords, n)

    return distance_matrix, coords_matrix

def experiment(matrix: np.ndarray, algorithm: Callable[[np.ndarray], tuple[list[int], list[int]]], runs=100):
    total_costs = []
    min_cost = float('inf')
    max_cost = float('-inf')
    best_cycle1 = []
    best_cycle2 = []

    for i in range(runs):
        cycle1, cycle2 = algorithm(matrix)
        length1 = cycle_length(cycle1, matrix)
        length2 = cycle_length(cycle2, matrix)
        total = length1 + length2
        total_costs.append(total)

        if total < min_cost:
            min_cost = total
            best_cycle1 = cycle1
            best_cycle2 = cycle2
        if total > max_cost:
            max_cost = total

    avg_cost = sum(total_costs) / runs
    return avg_cost, min_cost, max_cost, best_cycle1, best_cycle2

def run_test(algorithm_name: str, distance_matrix: np.ndarray, positions: np.ndarray, algorithm: Callable[[np.ndarray], tuple[list[int], list[int]]], visualize: bool = False):
    avg_alg, min_alg, max_alg, best_cycle1, best_cycle2 = experiment(distance_matrix, algorithm)
    if visualize: visualize_cycles(best_cycle1, best_cycle2, positions)
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

def visualize_cycles(cycle1: list[int], cycle2: list[int], positions: np.ndarray) -> None:
    plt.figure(figsize=(8, 8))
    
    def plot_cycle(cycle, color):
        x = [positions[i, 0] for i in cycle] + [positions[cycle[0], 0]]
        y = [positions[i, 1] for i in cycle] + [positions[cycle[0], 1]]
        plt.plot(x, y, marker='o', color=color, linestyle='-')
    
    plot_cycle(cycle1, 'blue')
    plot_cycle(cycle2, 'red')
    
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.title("Visualization of Two Cycles")
    plt.show()