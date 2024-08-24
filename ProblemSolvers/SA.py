from scipy.optimize import dual_annealing

# Función objetivo para SA
def objective(x):
    penalties = 0
    total = sum(x)
    
    if total != total_pullovers - pullovers_para_arbitros_y_profesores:
        penalties += 1000
    
    for i in range(len(facultades)):
        if x[i] > atletas[facultades[i]]:
            penalties += 1000

    return penalties

bounds = [(0, total_pullovers)] * len(facultades)

result = dual_annealing(objective, bounds)
print(f"Mejor distribución de pullovers: {result.x}")
