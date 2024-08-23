import pulp

# Datos de entrada
facultades = ['FTur', 'Eko', 'Lex', 'FCom', 'ConFin', 'Psico', 'FLEx', 'FHS', 'MatCom', 'ISDi', 'Geo', 'IFAL', 'FBio', 'FQ', 'FAyL', 'FF', 'InSTec', 'FENHI']
atletas = {'FTur': 143, 'Eko': 178, 'Lex': 160, 'FCom': 160, 'ConFin': 122, 'Psico': 156, 'FHS': 85, 'MatCom': 122, 'ISDi': 73, 'Geo': 28, 'IFAL': 86, 'FBio': 84, 'FQ': 5, 'FAyL': 54, 'FF': 26, 'InSTec': 25, 'FENHI': 6}  # 'FLEx' no está presente
ranking = {'FTur': 2, 'Eko': 1, 'Lex': 3, 'FCom': 5, 'ConFin': 8, 'Psico': 9, 'FHS': 12, 'MatCom': 7, 'ISDi': 11, 'Geo': 15, 'IFAL': 14, 'FBio': 10, 'FQ': 18, 'FAyL': 13, 'FF': 16, 'InSTec': 17, 'FENHI': 19, 'FLEx': 4}
total_pullovers = 1000
pullovers_para_arbitros_y_profesores = 100
pullovers_para_aaac = 30
colores = ['AC', 'AO', 'G']
pullovers_disponibles = {'AC': 336, 'AO': 364, 'G': 300}
preferencias = {'FTur' : 'AC', 'Eko' : 'G', 'Lex' : 'AO', 'FCom' : 'AO', 'ConFin' : 'G', 'Psico' : 'G', 'FHS' : 'G', 'MatCom' : 'AC', 'ISDi' : 'G', 'Geo' : 'AO', 'IFAL' : 'G', 'FBio' : 'AO', 'FQ' : 'AO', 'FAyL' : 'AC', 'FF' : 'G', 'InSTec' : 'AO', 'FLEx' : 'AO'}

# Crear problema
prob = pulp.LpProblem("Distribución_de_pulovers", pulp.LpMinimize)

# Variables de decisión
x = {i: pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in facultades}
y = {(i, j): pulp.LpVariable(f"y_{i}_{j}", cat="Binary") for i in facultades for j in colores}
z = {(i, j): pulp.LpVariable(f"z_{i}_{j}", lowBound=0, cat="Continuous" ) for i in facultades for j in colores}

proporciones = {i: pulp.LpVariable(f"proporción_{i}", lowBound=0) for i in facultades}
diferencia = {i: pulp.LpVariable(f"diferencia_{i}", lowBound=0) for i in facultades}

### Restricciones que deben cumplirse siempre
# Restricción: la suma de pullovers asignados a todas las facultades debe ser igual al total disponible
prob += pulp.lpSum(x[i] for i in facultades) == total_pullovers

# Restricción: cada facultad recibe exactamente un color
for i in facultades:
    prob += pulp.lpSum(y[i, j] for j in colores) == 1
    for j in colores:
        if y[i, j]:
            prob += x[i] <= pullovers_disponibles[j]