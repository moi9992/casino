import random

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

GAIN = {5: 750, 4: 11, 3: 1, 2: 0, 1: 0, 0: 0}

NOMBRE_TIRER = range(1, 81)


def compter_bons(choix_joueur, tirage):
    bons_numero = 0
    for nombre in choix_joueur:
        if nombre in tirage:
            bons_numero += 1
    return bons_numero


def demander_numeros():
    while True:
        texte = input("choisissez vos 5 numéro allant de 1 a 80 : ")
        numeros = lire_numeros(texte)
        if numeros is not None:
            return numeros
        else:
            print("choisissez une option valide")


def lire_numeros(texte):
    morceaux = texte.split()
    numeros = []
    try:
        for m in morceaux:
            numeros.append(int(m))
    except ValueError:
        return None
    if len(numeros) != 5:
        return None
    if min(numeros) < 1 or max(numeros) > 80:
        return None
    if len(set(numeros)) != 5:
        return None
    return numeros


def tirer_numeros():
    tirage = random.sample(NOMBRE_TIRER, 20)
    return tirage


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
            tirage = tirer_numeros()

            choix_joueur = demander_numeros()
            bons_numero = compter_bons(choix_joueur, tirage)

            print(choix_joueur, tirage, bons_numero)

            if bons_numero == 5:
                print("jackpot")
            elif bons_numero == 4:
                print("gros gain")
            elif bons_numero == 3:
                print("petit gain")
            else:
                print("perdu")

            gain = mise * GAIN[bons_numero]
            solde += gain
            print("gain gagné : ", gain)

            sauvegarder_solde(solde)

        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
