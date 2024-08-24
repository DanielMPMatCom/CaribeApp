from deap import base, creator, tools, algorithms
import random

# Datos de ejemplo
facultades = ['A', 'B', 'C']
atletas = {'A': 15, 'B': 8, 'C': 20}
total_pullovers = 80
pullovers_para_arbitros_y_profesores = 100

# Crear clases y funciones para el algoritmo genético
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def eval_individual(individual):
    penalties = 0
    total = sum(individual)
    
    # Penalización si no se cumplen las restricciones
    if total != total_pullovers - pullovers_para_arbitros_y_profesores:
        penalties += 1000
    
    for i in range(len(facultades)):
        if individual[i] > atletas[facultades[i]]:
            penalties += 1000

    return penalties,

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 0, total_pullovers)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_int, n=len(facultades))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", eval_individual)

# Algoritmo genético
population = toolbox.population(n=300)
algorithms.eaSimple(population, toolbox, cxpb=0.7, mutpb=0.2, ngen=50, verbose=True)

# Mejor individuo
best_ind = tools.selBest(population, 1)[0]
print(f"Mejor distribución de pullovers: {best_ind}")
