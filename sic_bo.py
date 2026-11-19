import random

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

GAIN_TOTAL = {
    4: 51,
    5: 31,
    6: 18,
    7: 13,
    8: 9,
    9: 7,
    10: 7,
    11: 7,
    12: 7,
    13: 9,
    14: 13,
    15: 18,
    16: 31,
    17: 51,
}


def demander_numero():
    while True:
        choix_numero = input("choisissez un chiffre allant de 1 à 6 : ")
        try:
            choix_numero = int(choix_numero)
            if choix_numero >= 1 and choix_numero <= 6:
                return choix_numero
            else:
                print("choisissez une option valide")
        except ValueError:
            print("erreur")


def demander_pari(options):
    while True:
        choix = (
            input("voulez vous choisir " + ", ".join(options) + " : ").strip().lower()
        )
        if choix in options:
            return choix
        else:
            print("choisissez une option valide")


def demander_total():
    while True:
        choix_total = input("choisissez votre numéro allant de 4 à 17 : ")
        try:
            choix_total = int(choix_total)
            if choix_total >= 4 and choix_total <= 17:
                return choix_total
            else:
                print("choisissez une option valide")
        except ValueError:
            print("erreur")


def est_triple(dee_tirer):
    triple = False

    if dee_tirer[0] == dee_tirer[1] == dee_tirer[2]:
        triple = True
    return triple


def gain_numero(dee_tirer, choix_numero, mise):
    if choix_numero in dee_tirer:
        nb_sorties = dee_tirer.count(choix_numero)
        gain = mise * (nb_sorties + 1)
        return gain
    else:
        return 0


def lancer_des():
    dee_tirer = []

    for i in range(3):
        tirage = random.randint(1, 6)
        dee_tirer.append(tirage)
    return dee_tirer


def trouver_taille(dee_tirer):
    triple = est_triple(dee_tirer)
    total = sum(dee_tirer)
    if triple == True:
        taille = 0
    elif total >= 4 and total <= 10:
        taille = "petit"
    else:
        taille = "grand"
    return taille


def jouer():
    solde = charger_solde()

    while True:
        menu = input("jouer ou stop : ").strip().lower()
        if menu == "jouer":
            if not peut_jouer(solde):
                print("solde insuffisant")
                continue
            print("solde disponible : ", solde)
            choix_taille = None
            choix_total = None
            choix_numero = None
            choix_triple = None
            options = ["petit", "grand", "pari", "numéro", "triple", "lancer"]
            while True:
                if len(options) == 1:
                    break
                if not peut_jouer(solde):
                    print("solde insuffisant lancement des dée")
                    break
                choix = demander_pari(options)
                if choix == "petit":
                    mise_taille = demander_mise(solde)
                    solde -= mise_taille
                    choix_taille = "petit"
                    options.remove("petit")
                    options.remove("grand")
                elif choix == "grand":
                    mise_taille = demander_mise(solde)
                    solde -= mise_taille
                    choix_taille = "grand"
                    options.remove("grand")
                    options.remove("petit")
                elif choix == "pari":
                    mise_total = demander_mise(solde)
                    solde -= mise_total
                    choix_total = demander_total()
                    options.remove("pari")
                elif choix == "numéro":
                    mise_numero = demander_mise(solde)
                    solde -= mise_numero
                    choix_numero = demander_numero()
                    options.remove("numéro")
                elif choix == "triple":
                    mise_triple = demander_mise(solde)
                    solde -= mise_triple
                    choix_triple = "triple"
                    options.remove("triple")
                elif choix == "lancer":
                    break

            dee_tirer = lancer_des()

            total = sum(dee_tirer)

            triple = est_triple(dee_tirer)

            print(dee_tirer, total)
            gain_total = 0

            taille = trouver_taille(dee_tirer)

            if choix_taille is not None:
                if choix_taille == taille:
                    print("choix : gagné")
                    gain = mise_taille * 2
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print("choix : perdu")

            if choix_total is not None:
                if choix_total == total:
                    print("pari : gagné")
                    gain = mise_total * GAIN_TOTAL[total]
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print("pari : perdu")

            if choix_numero is not None:
                gain = gain_numero(dee_tirer, choix_numero, mise_numero)
                if gain > 0:
                    print("numéro : gagné")
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print("numéro : perdu")

            if choix_triple is not None:
                if triple == True:
                    print("triple : gagné")
                    gain = mise_triple * 31
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print("triple : perdu")

            print("gain total gagné : ", gain_total)
            sauvegarder_solde(solde)

        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
