import numpy as np
import utils

def regret_heuristic(distance_matrix: np.ndarray) -> tuple[list[int], list[int]]:
    cycle1, cycle2, remaining_nodes = utils.initialize_cycles(distance_matrix)
    
    while remaining_nodes:
        best_candidate = None
        best_cycle = None
        best_regret = -float('inf')
        
        for candidate in remaining_nodes:
            regret1, _, _ = utils.calculate_regret(distance_matrix, cycle1, candidate)
            regret2, _, _ = utils.calculate_regret(distance_matrix, cycle2, candidate)
            
            if regret1 > best_regret:
                best_candidate, best_cycle = candidate, cycle1
                best_regret = regret1
            if regret2 > best_regret:
                best_candidate, best_cycle = candidate, cycle2
                best_regret = regret2
        
        utils.insert_into_cycle(distance_matrix, best_cycle, best_candidate)
        remaining_nodes.remove(best_candidate)
    
    return cycle1, cycle2