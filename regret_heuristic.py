import numpy as np
from utils import initialize_cycles, calculate_regret, insert_into_cycle

def regret_heuristic(distance_matrix: np.ndarray) -> tuple[list[int], list[int]]:
    cycle1, cycle2, remaining_nodes = initialize_cycles(distance_matrix)
    
    target_size1 = (len(distance_matrix) + 1) // 2
    target_size2 = len(distance_matrix) // 2
    
    while remaining_nodes:
        best_candidate = None
        best_cycle = None
        best_regret = -float('inf')
        
        for candidate in remaining_nodes:
            regret1, increase1, _ = calculate_regret(distance_matrix, cycle1, candidate)
            regret2, increase2, _ = calculate_regret(distance_matrix, cycle2, candidate)
            
            if regret1 > best_regret and len(cycle1) < target_size1:
                best_candidate, best_cycle = candidate, cycle1
                best_regret = regret1
            if regret2 > best_regret and len(cycle2) < target_size2:
                best_candidate, best_cycle = candidate, cycle2
                best_regret = regret2
        
        insert_into_cycle(distance_matrix, best_cycle, best_candidate)
        remaining_nodes.remove(best_candidate)
    
    return cycle1, cycle2