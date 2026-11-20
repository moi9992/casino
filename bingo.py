import random

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

nombre_tirer = range(1, 76)


def a_bingo(grille):
    for i in range(5):
        if grille[i].count("x") == 5:
            return True

    for j in range(5):
        compteur = 0

        for i in range(5):
            if grille[i][j] == "x":
                compteur += 1

        if compteur == 5:
            return True

    compteur_diagonale = 0

    for i in range(5):
        if grille[i][i] == "x":
            compteur_diagonale += 1

    compteur_diagonale2 = 0

    for i in range(5):
        if grille[i][4 - i] == "x":
            compteur_diagonale2 += 1

    if compteur_diagonale == 5 or compteur_diagonale2 == 5:
        return True

    return False


def calculer_multiplicateur(nb_boules):
    if nb_boules <= 20:
        return 10
    elif nb_boules <= 25:
        return 4
    elif nb_boules <= 30:
        return 3
    elif nb_boules <= 35:
        return 2
    else:
        return 0


def creer_grille():
    numeros_cartes = random.sample(nombre_tirer, 25)

    grille = []

    for i in range(5):
        debut = i * 5
        grille.append(numeros_cartes[debut : debut + 5])

    grille[2][2] = "x"
    return grille


def tirer_jusqu_au_bingo(grille):
    boules = list(range(1, 76))
    random.shuffle(boules)

    bingo = False

    nb_boules = 0

    while bingo == False:
        boule = boules.pop()
        nb_boules += 1

        for i in range(5):
            if boule in grille[i]:
                colonne = grille[i].index(boule)
                grille[i][colonne] = "x"

        bingo = a_bingo(grille)

    return nb_boules


def jouer():
    solde = charger_solde()

    while True:
        menu = input("jouer ou stop : ").lower().strip()
        if menu == "jouer":
            if not peut_jouer(solde):
                print("solde insuffisant")
                continue
            print("solde disponible : ", solde)
            mise = demander_mise(solde)
            solde = solde - mise

            grille = creer_grille()

            for i in range(5):
                print(grille[i])

            nb_boules = tirer_jusqu_au_bingo(grille)

            print("\nBINGO")
            print("nombre de boules avant d'avoir un bingo : ", nb_boules)
            for i in range(5):
                print(grille[i])

            gain = mise * calculer_multiplicateur(nb_boules)
            solde += gain
            print("gain gagné : ", gain)

            sauvegarder_solde(solde)
        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
