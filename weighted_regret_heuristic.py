import numpy as np
import utils

def weighted_regret_heuristic(distance_matrix: np.ndarray, w1: float = 1.0, w2: float = -1.0) -> tuple[list[int], list[int]]:
    cycle1, cycle2, remaining_nodes = utils.initialize_cycles(distance_matrix)
    
    while remaining_nodes:
        best_candidate = None
        best_cycle = None
        best_weighted_value = -float('inf')
        
        for candidate in remaining_nodes:
            regret1, increase1, _ = utils.calculate_regret(distance_matrix, cycle1, candidate)
            regret2, increase2, _ = utils.calculate_regret(distance_matrix, cycle2, candidate)
            
            weighted_value1 = w1 * regret1 + w2 * increase1
            weighted_value2 = w1 * regret2 + w2 * increase2
            
            if weighted_value1 > best_weighted_value:
                best_candidate, best_cycle = candidate, cycle1
                best_weighted_value = weighted_value1
            if weighted_value2 > best_weighted_value:
                best_candidate, best_cycle = candidate, cycle2
                best_weighted_value = weighted_value2
        
        utils.insert_into_cycle(distance_matrix, best_cycle, best_candidate)
        remaining_nodes.remove(best_candidate)
    
    return cycle1, cycle2