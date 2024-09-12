from PuLP_Solver import PuLP_Solver as solver
import string
import random

def test_1():
    print(" Test 1")
    solution = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo"],
        athletes={"Derecho": 100, "MatCom": 80, "FBio": 50, "Turismo": 90},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3},
        available_pullovers={"AC": 150, "B": 100},
        pullovers_for_referees_and_teachers=0,
        pullovers_for_aaac=0,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )

    print(solution)

def test_2():
    print("Test 2")
    solution = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo", "FLEX", "Psico", "FAYL"],
        athletes={"Derecho": 100, "MatCom": 80, "FBio": 60, "Turismo": 90, "FLEX": 20, "Psico": 40, "FAYL": 30},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3, "FLEX": 5, "Psico": 6, "FAYL": 7},
        available_pullovers={"AC": 100, "B": 100, "N": 150},
        pullovers_for_referees_and_teachers=20,
        pullovers_for_aaac=10,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )

    print(solution)    

def test_3():
    print("Test 3")
    solution = solver(
        faculties=list(string.ascii_uppercase),
        athletes={letter: random.randint(50, 100) for letter in string.ascii_uppercase},
        ranking={letter: indice for indice, letter in enumerate(string.ascii_uppercase, start=1)},
        available_pullovers={"B": 300, "AC":300, "R": 300, "A": 300},
        pullovers_for_referees_and_teachers=100,
        pullovers_for_aaac=50,
        preferences={}
    )

    print(solution)

def test_infactible():
    print("Infactible Run")
    solution = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo", "FLEX", "Psico", "FAYL"],
        athletes={"Derecho": 100, "MatCom": 80, "FBio": 60, "Turismo": 90, "FLEX": 20, "Psico": 40, "FAYL": 30},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3, "FLEX": 5, "Psico": 6, "FAYL": 7},
        available_pullovers={"AC": 5, "B": 1, "N": 1},
        pullovers_for_referees_and_teachers=0,
        pullovers_for_aaac=0,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )

    print(solution)