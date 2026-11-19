import random
import time

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

CRASH_MAX = 15


def demander_objectif(message):
    while True:
        reponse = input(message).replace(",", ".")
        try:
            reponse = float(reponse)
            if objectif_valide(reponse):
                return reponse
            else:
                print("choisissez une option valide")
        except ValueError:
            print("erreur")


def objectif_valide(objectif):
    return objectif > 1 and objectif <= CRASH_MAX


def tirer_crash():
    crash = 1 / (1 - random.random())
    crash = min(crash, CRASH_MAX)
    return round(crash, 2)


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
            objectif = demander_objectif("votre objectif allant de 1.01 a 15 compris: ")
            crash = tirer_crash()

            multiplicateur = 1

            while multiplicateur < crash:
                print("multiplicateur de gain : ", multiplicateur)
                multiplicateur *= 1.05
                multiplicateur = round(multiplicateur, 2)
                time.sleep(0.2)

            print("crash à : ", crash)

            if objectif <= crash:
                print("pari : gagné")
                gain = round((objectif * mise), 2)
                solde += gain
                print("gain gagné : ", gain)
            else:
                print("pari : perdu")

            sauvegarder_solde(solde)

        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
