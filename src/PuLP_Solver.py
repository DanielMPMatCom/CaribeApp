import pulp, random, time

def calculate_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.6f} seconds")
        return result
    return wrapper

@calculate_execution_time
def PuLP_Solver(
    faculties,
    athletes,
    ranking,
    available_pullovers,
    pullovers_for_referees,
    pullovers_for_teachers,
    pullovers_for_aaac,
    color_for_referees=None,
    color_for_teachers=None,
    color_for_aaac=None,
    preferences={},
):
    colors = [color for color in available_pullovers.keys()]

        
    total_pullovers = sum(amount for amount in available_pullovers.values())

    if(len(faculties) > total_pullovers):
        raise ValueError("No hay suficientes pullovers para repartir a todas las facultades")
    
    new_total = total_pullovers

    assigned_pullovers = {}

    # Assigning pullovers to referees, teachers, and AAAC
    for group in ["Árbitros", "Profesores", "AAAC"]:
        if group == "AAAC":
            amount = pullovers_for_aaac
            pref_color = color_for_aaac
        elif group == "Pofesores":
            amount = pullovers_for_teachers
            pref_color = color_for_teachers
        else: 
            amount = pullovers_for_referees
            pref_color = color_for_referees

        available = [color for color in available_pullovers if available_pullovers[color] >= amount]
        
        if not available:
            continue
        
        if pref_color in available:
            choosen_color = pref_color
        else:
            choosen_color = random.choice(available)

        available_pullovers[choosen_color] -= amount
        assigned_pullovers[group] = (amount, choosen_color)
        new_total -= amount

    # Initial assignment for faculties with fewer than 10 athletes
    faculties_under_10 = {
        i: athletes[i] for i in faculties if i in athletes and athletes[i] < 10
    }

    for fac, num in faculties_under_10.items():
        preferred_color = preferences.get(fac, random.choice(colors))
        available_pullovers[preferred_color] -= num
        new_total -= num
        assigned_pullovers[fac] = (num, preferred_color)
    remaining_faculties = [i for i in faculties if i not in faculties_under_10]

    if not remaining_faculties:
        return assigned_pullovers

    # Create the optimization problem
    prob = pulp.LpProblem("Pullover_Distribution", pulp.LpMinimize)

    # Define decision variables
    x = {
        i: pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer")
        for i in remaining_faculties
    }
    y = {
        (i, j): pulp.LpVariable(f"y_{i}_{j}", cat="Binary")
        for i in remaining_faculties
        for j in colors
    }
    proportions = {
        i: pulp.LpVariable(f"proportion_{i}", lowBound=0) for i in remaining_faculties
    }
    difference = {
        i: pulp.LpVariable(f"difference_{i}", lowBound=0) for i in remaining_faculties
    }
    z = {
        (i, j): pulp.LpVariable(f"z_{i}_{j}", lowBound=0, cat="Continuous")
        for i in remaining_faculties
        for j in colors
    }

    # Constraint: the sum of the pullovers assigned to all faculties must equal the total available
    prob += pulp.lpSum(x[i] for i in remaining_faculties) == new_total

    # Constraint: each faculty receives exactly one color
    for i in remaining_faculties:
        prob += pulp.lpSum(y[i, j] for j in colors) == 1
        for j in colors:
            if y[i, j]:
                prob += x[i] <= available_pullovers[j]

    # Constraint: each faculty must receive at least 10 pullovers if they have 10 or more athletes
    for i in remaining_faculties:
        prob += x[i] >= 10

    # Constraint: the sum of pullovers assigned of the same color must not exceed the amount available for that color
    for j in colors:
        prob += (
            pulp.lpSum(z[i, j] for i in remaining_faculties) <= available_pullovers[j]
        )

    # Relationship between z[i, j], x[i], y[i, j]
    for i in remaining_faculties:
        for j in colors:
            prob += z[i, j] <= x[i]
            prob += z[i, j] <= y[i, j] * new_total
            prob += z[i, j] >= x[i] - (1 - y[i, j]) * new_total

    # Additional constraints
    mean_proportions = new_total / sum(athletes.values())

    for i in remaining_faculties:
        if i in athletes:  # Only if we have the athlete data
            # Constraint to link proportions[i] with x[i] and athletes[i]
            prob += proportions[i] * athletes[i] == x[i]
            # Absolute difference between the proportion and the mean
            prob += difference[i] >= proportions[i] - mean_proportions
            prob += difference[i] >= mean_proportions - proportions[i]

    # Function to add constraints iteratively
    def add_constraint(constraint_function, priority_level):
        prob_copy = prob.copy()  # Create a copy of the current problem
        constraint_function(prob_copy)  # Try adding the constraint
        prob_copy.solve()
        if pulp.LpStatus[prob_copy.status] == "Optimal":
            # If the problem is feasible with the new constraint, add it
            constraint_function(prob)
        else:
            print(f"Priority {priority_level} constraint ignored due to conflict.")

    # Functions for each constraint
    def constraint_0(prob):
        for i in remaining_faculties:
            if i in athletes:  # Apply only if athlete data is available
                prob += x[i] <= athletes[i]

    def constraint_1(prob):
        for a in remaining_faculties:
            for b in remaining_faculties:
                if ranking[a] < ranking[b]:
                    prob += x[a] >= x[b]

    def constraint_2(prob):
        if i in faculties_under_10:
            prob += x[i] == athletes[i]

    def constraint_3(prob):
        for a in remaining_faculties:
            for b in remaining_faculties:
                if a in athletes and b in athletes and athletes[a] > athletes[b]:
                    prob += x[a] >= x[b]

    def constraint_4(prob):
        for i in remaining_faculties:
            preferred_color = preferences.get(i, None)
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
    prob += pulp.lpSum(difference[i] for i in remaining_faculties if i in athletes)

    # Solve the final problem
    prob.solve(pulp.PULP_CBC_CMD(timeLimit=30, msg=False))

    # Update available pullovers after the assignment
    for i in remaining_faculties:
        assigned_amount = pulp.value(x[i])
        assigned_color = None
        for j in colors:
            if pulp.value(y[i, j]) == 1:
                assigned_color = j
                available_pullovers[j] -= assigned_amount
                break
        assigned_pullovers[i] = (assigned_amount, assigned_color)

    

    remaining_pullovers = {}
    for color in colors:
        remaining_pullovers.update({color: 0})

    assigned_pullovers = dict(sorted(
    assigned_pullovers.items(),
    key=lambda item: (item[0] not in ranking, ranking.get(item[0], float('inf')))
    ))


    for item in assigned_pullovers:
        if item in athletes:
            if athletes[item] < assigned_pullovers[item][0]:
                remaining_pullovers[assigned_pullovers[item][1]] += (assigned_pullovers[item][0] - athletes[item])
                assigned_pullovers[item] = (athletes[item], assigned_pullovers[item][1])
            elif athletes[item] > assigned_pullovers[item][0]:
                if remaining_pullovers[assigned_pullovers[item][1]]:
                    aditional_pullovers = min(remaining_pullovers[assigned_pullovers[item][1]], athletes[item] - assigned_pullovers[item][0])
                    remaining_pullovers[assigned_pullovers[item][1]] -= aditional_pullovers
                    athletes[item] += aditional_pullovers


    print("\nPullovers Restantes de cada Color: ")
    for color in remaining_pullovers:
        print(f"{remaining_pullovers[color]} pullovers de color {color}")
    print("\n")

    return assigned_pullovers