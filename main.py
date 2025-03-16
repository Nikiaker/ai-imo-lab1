from nearest_neighbor import nearest_neighbor
from greedy_cycle import greedy_cycle
from regret_heuristic import regret_heuristic
from weighted_regret_heuristic import weighted_regret_heuristic
import utils

if __name__ == "__main__":
    kroa200_matrix, kroa200_coords = utils.load_from_tsp('datasets/kroA200.tsp')
    krob200_matrix, krob200_coords = utils.load_from_tsp('datasets/kroB200.tsp')

    print("Eksperymenty dla kroA200:")
    utils.run_test("Nearest Neighbor", kroa200_matrix, kroa200_coords, nearest_neighbor)
    utils.run_test("Greedy Cycle", kroa200_matrix, kroa200_coords, greedy_cycle)
    utils.run_test("Regret Heuristic", kroa200_matrix, kroa200_coords, regret_heuristic)
    utils.run_test("Weighted Regret Heuristic", kroa200_matrix, kroa200_coords, weighted_regret_heuristic)

    print("\nEksperymenty dla kroB200:")
    utils.run_test("Nearest Neighbor", krob200_matrix, krob200_coords, nearest_neighbor)
    utils.run_test("Greedy Cycle", krob200_matrix, krob200_coords, greedy_cycle)
    utils.run_test("Regret Heuristic", krob200_matrix, krob200_coords, regret_heuristic)
    utils.run_test("Weighted Regret Heuristic", krob200_matrix, krob200_coords, weighted_regret_heuristic)
