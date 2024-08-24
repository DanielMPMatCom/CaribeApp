import pulp, random

class PuLP_Solver():
    def __init__(self, faculties, athletes, ranking, available_pullovers, p_referees_and_teachers, p_aaac, preferences = {}):
        self.faculties = faculties
        self.athletes = athletes
        self.ranking = ranking
        
        self.colors = [color for color in available_pullovers.keys()]
        self.total_pullovers = sum(amount for amount in available_pullovers.values())
        self.available_pullovers = available_pullovers

        self.pullovers_for_referees_and_teachers = p_referees_and_teachers
        self.pullovers_for_aaac = p_aaac

        self.preferences = preferences
        self.new_total = self.total_pullovers

        self._referees_teachers_aaac()
        self._faculties_under_10()
        self._main_problem()

    # Assigning pullovers to referees, teachers, and AAAC
    def _referees_teachers_aaac(self):
        self.assigned_pullovers = {}

        for group in ['referees', 'teachers', 'AAAC']:
            random_color = random.choice(self.colors)
            if group == 'AAAC':
                amount = self.pullovers_for_aaac
            else:
                amount = self.pullovers_for_referees_and_teachers // 2
            
            self.available_pullovers[random_color] -= amount
            self.assigned_pullovers[group] = (amount, random_color)
            self.new_total -= amount

    # Initial assignment for faculties with fewer than 10 athletes
    def _faculties_under_10(self):
        self.faculties_under_10 = {i: self.athletes[i] for i in self.faculties if i in self.athletes and self.athletes[i] < 10}

        for fac, num in self.faculties_under_10.items():
            preferred_color = self.preferences.get(fac, random.choice(self.colors))
            self.available_pullovers[preferred_color] -= num
            self.new_total -= num
            self.assigned_pullovers[fac] = (num, preferred_color)
        self.remaining_faculties = [i for i in self.faculties if i not in self.faculties_under_10]

    def _main_problem(self):
        # Create the optimization problem
        prob = pulp.LpProblem("Pullover_Distribution", pulp.LpMinimize)

        # Define decision variables
        x = {i: pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in self.remaining_faculties}
        y = {(i, j): pulp.LpVariable(f"y_{i}_{j}", cat="Binary") for i in self.remaining_faculties for j in self.colors}
        proportions = {i: pulp.LpVariable(f"proportion_{i}", lowBound=0) for i in self.remaining_faculties}
        difference = {i: pulp.LpVariable(f"difference_{i}", lowBound=0) for i in self.remaining_faculties}
        z = {(i, j): pulp.LpVariable(f"z_{i}_{j}", lowBound=0, cat="Continuous") for i in self.remaining_faculties for j in self.colors}

        # Constraint: the sum of the pullovers assigned to all faculties must equal the total available
        prob += pulp.lpSum(x[i] for i in self.remaining_faculties) == self.new_total

        # Constraint: each faculty receives exactly one color
        for i in self.remaining_faculties:
            prob += pulp.lpSum(y[i, j] for j in self.colors) == 1
            for j in self.colors:
                if y[i, j]:
                    prob += x[i] <= self.available_pullovers[j]

        # Constraint: each faculty must receive at least 1 pullover
        for i in self.remaining_faculties:
            prob += x[i] >= 1

        # Constraint: the sum of pullovers assigned of the same color must not exceed the amount available for that color
        for j in self.colors:
            prob += pulp.lpSum(z[i, j] for i in self.remaining_faculties) <= self.available_pullovers[j]

        # Relationship between z[i, j], x[i], y[i, j]
        for i in self.remaining_faculties:
            for j in self.colors:
                prob += z[i, j] <= x[i]
                prob += z[i, j] <= y[i, j] * self.new_total
                prob += z[i, j] >= x[i] - (1 - y[i, j]) * self.new_total

        # Additional constraints
        mean_proportions = self.new_total / sum(self.athletes.values())

        for i in self.remaining_faculties:
            if i in self.athletes:  # Only if we have the athlete data
                # Constraint to link proportions[i] with x[i] and athletes[i]
                prob += proportions[i] * self.athletes[i] == x[i]
                # Absolute difference between the proportion and the mean
                prob += difference[i] >= proportions[i] - mean_proportions
                prob += difference[i] >= mean_proportions - proportions[i]

        # Function to add constraints iteratively
        def add_constraint(constraint_function, priority_level):
            prob_copy = prob.copy()  # Create a copy of the current problem
            constraint_function(prob_copy)  # Try adding the constraint
            prob_copy.solve()
            if pulp.LpStatus[prob_copy.status] == 'Optimal':
                # If the problem is feasible with the new constraint, add it
                constraint_function(prob)
            else:
                print(f"Priority {priority_level} constraint ignored due to conflict.")

        # Functions for each constraint
        def constraint_0(prob):
            for i in self.remaining_faculties:
                if i in self.athletes:  # Apply only if athlete data is available
                    prob += x[i] <= self.athletes[i]

        def constraint_1(prob):
            for a in self.remaining_faculties:
                for b in self.remaining_faculties:
                    if self.ranking[a] < self.ranking[b]:
                        prob += x[a] >= x[b]

        def constraint_2(prob):
            if i in self.faculties_under_10:
                prob += x[i] == self.athletes[i]

        def constraint_3(prob):
            for a in self.remaining_faculties:
                for b in self.remaining_faculties:
                    if a in self.athletes and b in self.athletes and self.athletes[a] > self.athletes[b]:
                        prob += x[a] >= x[b]

        def constraint_4(prob):
            for i in self.remaining_faculties:
                preferred_color = self.preferences.get(i, None)
                if preferred_color:
                    prob += y[i, preferred_color] == 1

        # Add constraints in order of priority
        add_constraint(constraint_0, 0)
        add_constraint(constraint_1, 1)
        add_constraint(constraint_2, 2)
        add_constraint(constraint_3, 3)
        add_constraint(constraint_4, 4)

        # Objective function
        # Minimize the sum of absolute differences
        prob += pulp.lpSum(difference[i] for i in self.remaining_faculties if i in self.athletes)

        # Solve the final problem
        prob.solve(pulp.PULP_CBC_CMD(timeLimit=30))

        # Update available pullovers after the assignment
        for i in self.remaining_faculties:
            assigned_amount = pulp.value(x[i])
            assigned_color = None
            for j in self.colors:
                if pulp.value(y[i, j]) == 1:
                    assigned_color = j
                    self.available_pullovers[j] -= assigned_amount
                    break
            self.assigned_pullovers[i] = (assigned_amount, assigned_color)

        # Print the result
        total = 0
        ac = 0
        ao = 0
        g = 0
        for group, (amount, color) in self.assigned_pullovers.items():
            print(f"{group}: {amount} pullovers of color {color}")
            total += amount
            if color == 'AC':
                ac += amount
            elif color == 'AO':
                ao += amount
            else:
                g += amount

        print(f"\nTotal: {total} pullovers assigned")
        print(f'AC: {ac} pullovers')
        print(f'AO: {ao} pullovers')
        print(f'G: {g} pullovers')

# solution = PuLP_Solver(
#     ['FTur', 'Eko', 'Lex', 'FCom', 'ConFin', 'Psico', 'FLEx', 'FHS', 'MatCom', 'ISDi', 'Geo', 'IFAL', 'FBio', 'FQ', 'FAyL', 'FF', 'InSTec', 'FENHI'],
#     {'FTur': 143, 'Eko': 178, 'Lex': 160, 'FCom': 160, 'ConFin': 122, 'Psico': 156, 'FHS': 85, 'MatCom': 122, 'ISDi': 73, 'Geo': 28, 'IFAL': 86, 'FBio': 84, 'FQ': 5, 'FAyL': 54, 'FF': 26, 'InSTec': 25, 'FENHI': 6},
#     {'FTur': 2, 'Eko': 1, 'Lex': 3, 'FCom': 5, 'ConFin': 8, 'Psico': 9, 'FHS': 12, 'MatCom': 7, 'ISDi': 11, 'Geo': 15, 'IFAL': 14, 'FBio': 10, 'FQ': 18, 'FAyL': 13, 'FF': 16, 'InSTec': 17, 'FENHI': 19, 'FLEx': 4},
#     {'AC': 336, 'AO': 364, 'G': 300},
#     100, 30,
#     {'FTur' : 'AC', 'Eko' : 'G', 'Lex' : 'AO', 'FCom' : 'AO', 'ConFin' : 'G', 'Psico' : 'G', 'FHS' : 'G', 'MatCom' : 'AC', 'ISDi' : 'G', 'Geo' : 'AO', 'IFAL' : 'G', 'FBio' : 'AO', 'FQ' : 'AO', 'FAyL' : 'AC', 'FF' : 'G', 'InSTec' : 'AO', 'FLEx' : 'AO'}
# )