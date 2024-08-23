# Data
facultades = ['A', 'B', 'C']
colores = ['AC', 'R']

preferencias = {
    'A': 'AC',
    'B': 'R',
    'C': 'AC'
    }

atletas = {
    'A': 20,
    'B': 15,
    'C': 8
}

ranking = {
    'A': 1,
    'B': 2,
    'C': 3,
}

pullovers = {
    'AC': 70,
    'R': 60
}

arbitros_y_profesores = 80
aaac = 20

def eval_solution(solution):
    
    penalties = 0
    totals = [len(colores)]

    remnant = {}

    for f in facultades:
        colour, amount = solution[ranking[f]]
        remnant



def hill_climbing(solution, evaluation, branch, depth):
    pass

