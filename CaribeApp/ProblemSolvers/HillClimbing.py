import random

# Función de evaluación
def eval_solution(solution):
    penalties = 0
    total = sum(solution)
    
    if total != total_pullovers - pullovers_para_arbitros_y_profesores:
        penalties += 1000
    
    for i in range(len(facultades)):
        if solution[i] > atletas[facultades[i]]:
            penalties += 1000

    return penalties

# Algoritmo de Hill Climbing
def hill_climbing():
    current_solution = [random.randint(0, total_pullovers) for _ in facultades]
    current_eval = eval_solution(current_solution)

    for _ in range(10000):
        new_solution = current_solution[:]
        idx = random.randint(0, len(facultades) - 1)
        new_solution[idx] = random.randint(0, total_pullovers)
        new_eval = eval_solution(new_solution)
        
        if new_eval < current_eval:
            current_solution = new_solution
            current_eval = new_eval

    return current_solution

best_solution = hill_climbing()
print(f"Mejor distribución de pullovers: {best_solution}")
