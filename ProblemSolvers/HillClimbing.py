import random

# Datos de ejemplo
facultades = ['A', 'B', 'C']
atletas = {'A': 15, 'B': 8, 'C': 20}
total_pullovers = 120
pullovers_para_arbitros_y_profesores = 100

# Función de evaluación
def eval_solution(solution):
    penalties = 0
    total = sum(solution)
    
    # Penalidades generales
    if total != total_pullovers - pullovers_para_arbitros_y_profesores:
        penalties += 10000
    if total > total_pullovers - pullovers_para_arbitros_y_profesores:
         penalties += 10000
    
    # Penalidades por facultad
    for i in range(len(facultades)):
            # Penalidad por diferencia entre atletas inscritos y pullovers asignados
            penalties += (atletas[facultades[i]] - solution[i]) ** 2

    return penalties

def recursive_hill_climbing(solution, depth, branches):

    if depth == 0:
        return solution, eval_solution(solution)

    step_evaluation = eval_solution(solution)
    step_solution = solution[:]

    for i in range(branches):

        new_solution = solution[:]
        new_index = random.randint(0, len(facultades) - 1)
        new_solution[new_index] = random.randint(0, atletas[facultades[new_index]])

        new_solution, new_evaluation = recursive_hill_climbing(new_solution, depth-1, branches)
        
        if new_evaluation < step_evaluation:
            step_solution = new_solution
            step_evaluation = new_evaluation
        
    return step_solution, step_evaluation
        

# Algoritmo de Hill Climbing
def hill_climbing():
    current_solution = [0 for _ in facultades]
    current_eval = eval_solution(current_solution)

    # Test
    first = True

    for _ in range(5000):
        new_solution = current_solution[:]
        idx = random.randint(0, len(facultades) - 1)
        new_solution[idx] = random.randint(0, atletas[facultades[idx]])
        new_eval = eval_solution(new_solution)
        
        if new_eval < current_eval:

            if new_eval > 20000 and first: 
                print(f"Evaluation of {new_solution} is {new_eval}")
                first = False

            current_solution = new_solution
            current_eval = new_eval

    return current_solution, current_eval

best_solution = hill_climbing()
best_solution_recursive = recursive_hill_climbing([0 for _ in facultades], 6, 10)

print()
print("-----------Testing area-----------")
print(f"Evaluation of [15, 8, 20]: {eval_solution([15, 8, 20])}")
print(f"Evaluation of [13, 5, 2]: {eval_solution([13, 5, 2])}")
print(f"Evaluation of [2, 2, 16]: {eval_solution([2, 2, 16])}")


print("-------End of testing area--------")
print()

print(f"Mejor distribución de pullovers: {best_solution}")
print(f"Mejor distribución de pullovers recursiva: {best_solution_recursive}")

