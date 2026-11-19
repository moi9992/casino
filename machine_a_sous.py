import random

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

SYMBOLE = ["cerise", "citron", "7", "banane"]


def calculer_multiplicateur(tirage):
    if tirage[0] == "7" and tirage[1] == "7" and tirage[2] == "7":
        return 8
    elif tirage[0] == tirage[1] == tirage[2]:
        return 5
    elif tirage[0] == tirage[1] or tirage[1] == tirage[2] or tirage[0] == tirage[2]:
        return 1
    else:
        return 0


def tirer_rouleaux():
    tirage_tirer = []
    for i in range(3):
        tirage = random.choice(SYMBOLE)
        tirage_tirer.append(tirage)

    return tirage_tirer


def jouer():
    solde = charger_solde()

    while True:
        menu = input("jouer ou stop : ").strip().lower()
        if menu == "jouer":
            if not peut_jouer(solde):
                print("solde insuffisant")
                continue
            print("solde disponible : ", solde)
            mise = demander_mise(solde)
            solde = solde - mise
            resultat = tirer_rouleaux()
            print(resultat)
            gain = mise * calculer_multiplicateur(resultat)
            solde += gain
            print("gain : ", gain)

            sauvegarder_solde(solde)
        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
