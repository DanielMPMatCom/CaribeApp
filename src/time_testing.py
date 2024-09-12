from PuLP_Solver import PuLP_Solver as solver

def test_1():
    print("First Run")
    first_run = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo"],
        athletes={"Derecho": 100, "MatCom": 80, "FBio": 50, "Turismo": 90},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3},
        available_pullovers={"AC": 150, "B": 100},
        pullovers_for_referees_and_teachers=0,
        pullovers_for_aaac=0,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )

    print(first_run)

def test_2():
    print("Second Run")
    second_run = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo", "FLEX", "Psico"],
        athletes={"Derecho": 100, "MatCom": 80, "FBio": 60, "Turismo": 90, "FLEX": 20, "Psico": 40},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3, "FLEX": 5, "Psico": 6},
        available_pullovers={"AC": 100, "B": 100, "N": 150},
        pullovers_for_referees_and_teachers=20,
        pullovers_for_aaac=10,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )

    print(second_run)

def test_3():
    print("Third Run")
    third_run = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo", "FLEX", "Psico", "FAYL"],
        athletes={"Derecho": 100, "MatCom": 80, "FBio": 60, "Turismo": 90, "FLEX": 20, "Psico": 40, "FAYL": 30},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3, "FLEX": 5, "Psico": 6, "FAYL": 7},
        available_pullovers={"AC": 100, "B": 100, "N": 150},
        pullovers_for_referees_and_teachers=20,
        pullovers_for_aaac=10,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )

    print(third_run)