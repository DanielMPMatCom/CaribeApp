import pulp, random

class PuLP_Solver():
    def __init__(self, facultades, atletas, ranking, pullovers_disponibles, p_arbitros_y_profesores, p_aaac,  preferencias = {}):
        self.facultades = facultades
        self.atletas = atletas
        self.ranking = ranking
        
        self.colores = [colour for colour in pullovers_disponibles.keys()]
        self.total_pullovers = sum(amount for amount in pullovers_disponibles.values())
        self.pullovers_disponibles = pullovers_disponibles

        self.pullovers_para_arbitros_y_profesores = p_arbitros_y_profesores
        self.pullovers_para_aaac = p_aaac

        self.preferencias = preferencias
        self.nuevo_total = self.total_pullovers

        self._arbitros_profesores_aaac()
        self._facultades_menores_10()
        self._problema_principal()

    # Asignación de pullovers a árbitros, profesores y AAAC
    def _arbitros_profesores_aaac(self):
        self.pullovers_asignados = {}

        for grupo in ['árbitros', 'profesores', 'AAAC']:
            color_aleatorio = random.choice(self.colores)
            if grupo == 'AAAC':
                cantidad = self.pullovers_para_aaac
            else:
                cantidad = self.pullovers_para_arbitros_y_profesores // 2
            
            self.pullovers_disponibles[color_aleatorio] -= cantidad
            self.pullovers_asignados[grupo] = (cantidad, color_aleatorio)
            self.nuevo_total -= cantidad

    # Asignación inicial para facultades con menos de 10 atletas
    def _facultades_menores_10(self):
        self.facultades_menores_10 = {i: self.atletas[i] for i in self.facultades if i in self.atletas and self.atletas[i] < 10}

        for fac, num in self.facultades_menores_10.items():
            color_preferido = self.preferencias.get(fac, random.choice(self.colores))
            self.pullovers_disponibles[color_preferido] -= num
            self.nuevo_total -= num
            self.pullovers_asignados[fac] = (num, color_preferido)
        self.facultades_restantes = [i for i in self.facultades if i not in self.facultades_menores_10]

    def _problema_principal(self):
        # Crear el problema de optimización
        prob = pulp.LpProblem("Distribucion_de_Pullovers", pulp.LpMinimize)

        # Definir variables de decisión
        x = {i: pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in self.facultades_restantes}
        y = {(i, j): pulp.LpVariable(f"y_{i}_{j}", cat="Binary") for i in self.facultades_restantes for j in self.colores}
        proporciones = {i: pulp.LpVariable(f"proporcion_{i}", lowBound=0) for i in self.facultades_restantes}
        diferencia = {i: pulp.LpVariable(f"diferencia_{i}", lowBound=0) for i in self.facultades_restantes}
        z = {(i, j): pulp.LpVariable(f"z_{i}_{j}", lowBound=0, cat="Continuous") for i in self.facultades_restantes for j in self.colores}

        # Restricción: la suma de los pullovers asignados a todas las facultades debe ser igual al total disponible
        prob += pulp.lpSum(x[i] for i in self.facultades_restantes) == self.nuevo_total

        # Restricción: cada facultad recibe exactamente un color
        for i in self.facultades_restantes:
            prob += pulp.lpSum(y[i, j] for j in self.colores) == 1
            # color_preferido = preferencias.get(i, None)
            # if color_preferido:
            #     prob += y[i, color_preferido] == 1
            for j in self.colores:
                if y[i,j]:
                    prob += x[i] <= self.pullovers_disponibles[j]

        # Restricción: cada facultad debe recibir al menos 1 pullover
        for i in self.facultades_restantes:
            prob += x[i] >= 1

        # Restricción: la suma de los pullovers asignados de un mismo color no debe exceder la cantidad disponible de ese color
        for j in self.colores:
            prob += pulp.lpSum(z[i, j] for i in self.facultades_restantes) <= self.pullovers_disponibles[j]

        # Relación entre z[i, j], x[i], y[i, j]
        for i in self.facultades_restantes:
            for j in self.colores:
                prob += z[i, j] <= x[i]
                prob += z[i, j] <= y[i, j] * self.nuevo_total
                prob += z[i, j] >= x[i] - (1 - y[i, j]) * self.nuevo_total

        # Restricciones adicionales
        media_proporciones = self.nuevo_total / sum(self.atletas.values())

        for i in self.facultades_restantes:
            if i in self.atletas:  # Solo si tenemos el dato de atletas
                # Restricción para ligar proporciones[i] con x[i] y atletas[i]
                prob += proporciones[i] * self.atletas[i] == x[i]
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
            for i in self.facultades_restantes:
                if i in self.atletas:  # Aplicar solo si el dato de atletas está disponible
                    prob += x[i] <= self.atletas[i]

        def restriction_1(prob):
            for a in self.facultades_restantes:
                for b in self.facultades_restantes:
                    if self.ranking[a] < self.ranking[b]:
                        prob += x[a] >= x[b]

        def restriction_2(prob):
            if i in self.facultades_menores_10:
                prob += x[i] == self.atletas[i]

        def restriction_3(prob):
            for a in self.facultades_restantes:
                for b in self.facultades_restantes:
                    if a in self.atletas and b in self.atletas and self.atletas[a] > self.atletas[b]:
                        prob += x[a] >= x[b]

        def restriction_4(prob):
            for i in self.facultades_restantes:
                color_preferido = self.preferencias.get(i, None)
                if color_preferido:
                    prob += y[i, color_preferido] == 1

        # Añadir restricciones en orden de prioridad
        add_constraint(restriction_0, 0)
        add_constraint(restriction_1, 1)
        add_constraint(restriction_2, 2)
        add_constraint(restriction_3, 3)
        add_constraint(restriction_4, 4)

        # Función objetivo
        # Minimizar la suma de las diferencias absolutas
        prob += pulp.lpSum(diferencia[i] for i in self.facultades_restantes if i in self.atletas)

        # Resolver el problema final
        prob.solve(pulp.PULP_CBC_CMD(timeLimit=30))

        # Actualizar pullovers disponibles después de la asignación
        for i in self.facultades_restantes:
            cantidad_asignada = pulp.value(x[i])
            color_asignado = None
            for j in self.colores:
                if pulp.value(y[i, j]) == 1:
                    color_asignado = j
                    self.pullovers_disponibles[j] -= cantidad_asignada
                    break
            self.pullovers_asignados[i] = (cantidad_asignada, color_asignado)

        # Imprimir el resultado
        total = 0
        ac = 0
        ao = 0
        g = 0
        for grupo, (cantidad, color) in self.pullovers_asignados.items():
            print(f"{grupo}: {cantidad} pullovers del color {color}")
            total += cantidad
            if color == 'AC':
                ac += cantidad
            elif color == 'AO':
                ao += cantidad
            else:
                g += cantidad

        print(f"\nTotal: {total} pullovers asignados")
        print(f'AC: {ac} pullovers')
        print(f'AO: {ao} pullovers')
        print(f'G: {g} pullovers')

solution = PuLP_Solver(
    ['FTur', 'Eko', 'Lex', 'FCom', 'ConFin', 'Psico', 'FLEx', 'FHS', 'MatCom', 'ISDi', 'Geo', 'IFAL', 'FBio', 'FQ', 'FAyL', 'FF', 'InSTec', 'FENHI'],
    {'FTur': 143, 'Eko': 178, 'Lex': 160, 'FCom': 160, 'ConFin': 122, 'Psico': 156, 'FHS': 85, 'MatCom': 122, 'ISDi': 73, 'Geo': 28, 'IFAL': 86, 'FBio': 84, 'FQ': 5, 'FAyL': 54, 'FF': 26, 'InSTec': 25, 'FENHI': 6},
    {'FTur': 2, 'Eko': 1, 'Lex': 3, 'FCom': 5, 'ConFin': 8, 'Psico': 9, 'FHS': 12, 'MatCom': 7, 'ISDi': 11, 'Geo': 15, 'IFAL': 14, 'FBio': 10, 'FQ': 18, 'FAyL': 13, 'FF': 16, 'InSTec': 17, 'FENHI': 19, 'FLEx': 4},
    {'AC': 336, 'AO': 364, 'G': 300},
    100, 30,
    {'FTur' : 'AC', 'Eko' : 'G', 'Lex' : 'AO', 'FCom' : 'AO', 'ConFin' : 'G', 'Psico' : 'G', 'FHS' : 'G', 'MatCom' : 'AC', 'ISDi' : 'G', 'Geo' : 'AO', 'IFAL' : 'G', 'FBio' : 'AO', 'FQ' : 'AO', 'FAyL' : 'AC', 'FF' : 'G', 'InSTec' : 'AO', 'FLEx' : 'AO'}
)