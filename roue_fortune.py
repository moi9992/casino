import random

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

ROUE = (
    ["1"] * 24 + ["2"] * 15 + ["5"] * 7 + ["10"] * 4 + ["20"] * 2 + ["joker"] + ["logo"]
)

GAIN = {"1": 1, "2": 2, "5": 5, "10": 10, "20": 20, "joker": 40, "logo": 40}


def demander_valeur():
    while True:
        choix_valeur = (
            input("choisissez 1, 2, 5, 10, 20, joker ou logo : ").strip().lower()
        )
        if choix_valeur in GAIN:
            return choix_valeur
        else:
            print("choisissez une option valide")


def tourner_roue():
    symbole = random.choice(ROUE)
    return symbole


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
            choix = demander_valeur()
            tirage = tourner_roue()
            print(tirage)
            if choix == tirage:
                gain = mise + mise * GAIN[choix]
                solde += gain
                print("tirage : gagné\ngain gagné : ", gain)
            else:
                print("tirage : perdu")

            sauvegarder_solde(solde)
        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
