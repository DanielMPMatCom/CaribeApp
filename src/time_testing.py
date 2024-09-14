from PuLP_Solver import PuLP_Solver as solver
import string
import random


def test_2_faculties():
    print("Test 2 faculties")
    solution = solver(
        faculties=["Derecho", "MatCom"],
        athletes={"Derecho": 50, "MatCom": 30},
        ranking={"Derecho": 1, "MatCom": 2},
        available_pullovers={"AC": 50, "B": 50},
        pullovers_for_referees=0,
        pullovers_for_teachers=0,
        pullovers_for_aaac=0,
        preferences={"Derecho": "AC", "MatCom": "AC"}
    )
    for item in solution:
        print(f"{item} : {solution[item]}")


def test_4_faculties():
    print(" Test 4 faculties")
    solution = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo"],
        athletes={"Derecho": 80, "MatCom": 50, "FBio": 50, "Turismo": 80},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3},
        available_pullovers={"AC": 650, "B": 100},
        pullovers_for_referees=0,
        pullovers_for_teachers=0,
        pullovers_for_aaac=0,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )
    for item in solution:
        print(f"{item} : {solution[item]}")


def test_7_faculties():
    print("Test 7 Faculties")
    solution = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo", "FLEX", "Psico", "FAYL"],
        athletes={"Derecho": 100, "MatCom": 80, "FBio": 60, "Turismo": 90, "FLEX": 20, "Psico": 40, "FAYL": 30},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3, "FLEX": 5, "Psico": 6, "FAYL": 7},
        available_pullovers={"AC": 100, "B": 100, "N": 150},
        pullovers_for_referees=10,
        pullovers_for_teachers=10,
        pullovers_for_aaac=10,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )
    for item in solution:
        print(f"{item} : {solution[item]}")

def test_11_faculties():
    print("Test 11 Faculties")
    solution = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo", "Psico", "FAYL", "Economía", "Física", "Geografía", 
                   "Medicina", "Ingeniería"],
        athletes={"Derecho": 120, "MatCom": 110, "FBio": 90, "Turismo": 80, "Psico": 70, "FAYL": 60, 
                  "Economía": 50, "Física": 40, "Geografía": 30, "Medicina": 100, "Ingeniería": 90},
        ranking={"Derecho": 1, "MatCom": 2, "FBio": 3, "Turismo": 4, "Psico": 5, "FAYL": 6, 
                 "Economía": 7, "Física": 8, "Geografía": 9, "Medicina": 10, "Ingeniería": 11},
        available_pullovers={"AC": 200, "B": 200, "N": 200},
        pullovers_for_referees=20,
        pullovers_for_teachers=20,
        pullovers_for_aaac=20,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "N", "Turismo": "AC", "Psico": "B", "FAYL": "N", 
                     "Economía": "AC", "Física": "B", "Geografía": "N", "Medicina": "AC", "Ingeniería": "B"}
    )
    for item in solution:
        print(f"{item} : {solution[item]}")

def test_16_faculties():
    print("Test 16 Faculties Feasible")
    solution = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo", "FLEX", "Psico", "FAYL", "Filología", "Filosofía", "Economía", "Arquitectura", "Medicina", "Agronomía", "Educación", "Informática", "Química"],
        athletes={
            "Derecho": 80, "MatCom": 75, "FBio": 60, "Turismo": 85, "FLEX": 50, 
            "Psico": 40, "FAYL": 35, "Filología": 60, "Filosofía": 70, "Economía": 90, 
            "Arquitectura": 65, "Medicina": 100, "Agronomía": 55, "Educación": 50, 
            "Informática": 70, "Química": 60
        },
        ranking={
            "Derecho": 1, "MatCom": 2, "FBio": 3, "Turismo": 4, "FLEX": 5, "Psico": 6, 
            "FAYL": 7, "Filología": 8, "Filosofía": 9, "Economía": 10, "Arquitectura": 11, 
            "Medicina": 12, "Agronomía": 13, "Educación": 14, "Informática": 15, "Química": 16
        },
        available_pullovers={"AC": 800, "B": 500, "N": 600, "R": 450},
        pullovers_for_referees=20,
        pullovers_for_teachers=15,
        pullovers_for_aaac=25,
        preferences={
            "Derecho": "AC", "MatCom": "B", "FBio": "N", "Turismo": "AC", "FLEX": "R", 
            "Psico": "B", "FAYL": "AC", "Filología": "R", "Filosofía": "N", 
            "Economía": "AC", "Arquitectura": "B", "Medicina": "N", "Agronomía": "R", 
            "Educación": "B", "Informática": "AC", "Química": "R"
        }
    )
    for item in solution:
        print(f"{item} : {solution[item]}")

def test_infactible():
    print("Infactible Run")
    solution = solver(
        faculties=["Derecho", "MatCom", "FBio", "Turismo", "FLEX", "Psico", "FAYL"],
        athletes={"Derecho": 100, "MatCom": 80, "FBio": 60, "Turismo": 90, "FLEX": 20, "Psico": 40, "FAYL": 30},
        ranking={"Derecho": 2, "MatCom": 1, "FBio": 4, "Turismo": 3, "FLEX": 5, "Psico": 6, "FAYL": 7},
        available_pullovers={"AC": 4, "B": 1, "N": 1},
        pullovers_for_referees=0,
        pullovers_for_teachers=0,
        pullovers_for_aaac=0,
        preferences={"Derecho": "AC", "MatCom": "B", "FBio": "B", "Turismo": "AC"}
    )
    for item in solution:
        print(f"{item} : {solution[item]}")

# test_2_faculties()
test_4_faculties()
# test_7_faculties()
# test_11_faculties()
# test_16_faculties()

# test_infactible()