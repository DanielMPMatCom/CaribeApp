import pulp, random


def PuLP_Solver(
    faculties,
    athletes,
    ranking,
    available_pullovers,
    pullovers_for_referees_and_teachers,
    pullovers_for_aaac,
    preferences={},
):
    colors = [color for color in available_pullovers.keys()]
    total_pullovers = sum(amount for amount in available_pullovers.values())

    new_total = total_pullovers

    assigned_pullovers = {}

    # Assigning pullovers to referees, teachers, and AAAC
    for group in ["referees", "teachers", "AAAC"]:
        random_color = random.choice(colors)
        if group == "AAAC":
            amount = pullovers_for_aaac
        else:
            amount = pullovers_for_referees_and_teachers // 2

        available_pullovers[random_color] -= amount
        assigned_pullovers[group] = (amount, random_color)
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

    # Constraint: each faculty must receive at least 1 pullover
    for i in remaining_faculties:
        prob += x[i] >= 1

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
    prob.solve(pulp.PULP_CBC_CMD(timeLimit=30))

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

    return assigned_pullovers


# assignation = PuLP_Solver(['ISRI', 'MATCOM', 'DER', 'TUR'], {'ISRI': 80, 'MATCOM': 80, 'DER': 20, 'TUR': 50}, {'ISRI': 1, 'MATCOM': 2, 'DER': 3, 'TUR': 5}, {'A': 100, 'B': 100, 'C': 100}, 50, 30, {'ISRI': 'A', 'MATCOM': 'B', 'DER': 'B', 'TUR': 'C'})

# for faculty, (pullovers, color) in assignation.items():
#     print(f'{faculty}: {pullovers} pullovers colour {color}')
