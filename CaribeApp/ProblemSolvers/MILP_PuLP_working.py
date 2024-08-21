import pulp

# Datos de entrada
facultades = ['FTur', 'Eko', 'Lex', 'FCom', 'ConFin', 'Psico', 'FLEx', 'FHS', 'MatCom', 'ISDi', 'Geo', 'IFAL', 'FBio', 'FQ', 'FAyL', 'FF', 'InSTec', 'FENHI']
atletas = {'FTur': 143, 'Eko': 178, 'Lex': 160, 'FCom': 160, 'ConFin': 122, 'Psico': 156, 'FHS': 85, 'MatCom': 122, 'ISDi': 73, 'Geo': 28, 'IFAL': 86, 'FBio': 84, 'FQ': 5, 'FAyL': 54, 'FF': 26, 'InSTec': 25, 'FENHI': 6}  # 'FLEx' no está presente
ranking = {'FTur': 2, 'Eko': 1, 'Lex': 3, 'FCom': 5, 'ConFin': 8, 'Psico': 9, 'FHS': 12, 'MatCom': 7, 'ISDi': 11, 'Geo': 15, 'IFAL': 14, 'FBio': 10, 'FQ': 18, 'FAyL': 13, 'FF': 16, 'InSTec': 17, 'FENHI': 19, 'FLEx': 4}
total_pullovers = 1000
pullovers_para_arbitros_y_profesores = 100
pullovers_para_aaac = 30
nuevo_total = total_pullovers - pullovers_para_arbitros_y_profesores - pullovers_para_aaac
colores = ['AC', 'AO', 'G']
pullovers_disponibles = {'AC': 336, 'AO': 364, 'G': 300}

# Crear el problema de optimización
prob = pulp.LpProblem("Distribucion_de_Pullovers", pulp.LpMinimize)

# Definir variables de decisión
x = {i: pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in facultades}
y = {(i, j): pulp.LpVariable(f"y_{i}_{j}", cat="Binary") for i in facultades for j in colores}
proporciones = {i: pulp.LpVariable(f"proporcion_{i}", lowBound=0) for i in facultades}
diferencia = {i: pulp.LpVariable(f"diferencia_{i}", lowBound=0) for i in facultades}

# Restricción: la suma de los pullovers asignados a todas las facultades debe ser igual al total disponible
prob += pulp.lpSum(x[i] for i in facultades) == nuevo_total

# Restricción: cada facultad recibe exactamente un color
for i in facultades:
    prob += pulp.lpSum(y[i, j] for j in colores) == 1
    prob += x[i] <= pulp.lpSum(y[i, j] * pullovers_disponibles[j] for j in colores)

# Restricción: cada facultad debe recibir al menos 1 pullover
for i in facultades:
    prob += x[i] >= 1

# Restricciones adicionales
media_proporciones = nuevo_total / sum(atletas.values())

for i in facultades:
    if i in atletas:  # Solo si tenemos el dato de atletas
        # Restricción para ligar proporciones[i] con x[i] y atletas[i]
        prob += proporciones[i] * atletas[i] == x[i]
        # Diferencia absoluta entre la proporción y la media
        prob += diferencia[i] >= proporciones[i] - media_proporciones
        prob += diferencia[i] >= media_proporciones - proporciones[i]

# Función para agregar restricciones de manera iterativa
def add_constraint(constraint_function, priority_level):
    prob_copy = prob.copy()  # Crear una copia del problema actual
    constraint_function(prob_copy)  # Intentar agregar la restricción
    prob_copy.solve()
    if pulp.LpStatus[prob_copy.status] == 'Optimal':
        # Si el problema es factible con la nueva restricción, la añadimos
        constraint_function(prob)
    else:
        print(f"Restricción de prioridad {priority_level} ignorada por conflicto.")

# Funciones para cada restricción
def restriction_0(prob):
    for i in facultades:
        if i in atletas:  # Aplicar solo si el dato de atletas está disponible
            prob += x[i] <= atletas[i]

def restriction_1(prob):
    for a in facultades:
        for b in facultades:
            if ranking[a] < ranking[b]:
                prob += x[a] >= x[b]

def restriction_2(prob):
    for i in facultades:
        if i in atletas and atletas[i] < 10:
            prob += x[i] == atletas[i]

def restriction_3(prob):
    for a in facultades:
        for b in facultades:
            if a in atletas and b in atletas and atletas[a] > atletas[b]:
                prob += x[a] >= x[b]

# Añadir restricciones en orden de prioridad
add_constraint(restriction_0, 0)
add_constraint(restriction_1, 1)
add_constraint(restriction_2, 2)
add_constraint(restriction_3, 3)

# Función objetivo
# Minimizar la suma de las diferencias absolutas
prob += pulp.lpSum(diferencia[i] for i in facultades if i in atletas)

# Resolver el problema final
prob.solve()

# Mostrar resultados
for i in facultades:
    print(f"Facultad {i}: {pulp.value(x[i])} pullovers")
    for j in colores:
        if pulp.value(y[i, j]) == 1:
            print(f"  - Color asignado: {j}")






