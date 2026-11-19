import random

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

NUMEROS_ROUGES = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]


def demander_douzaine():
    while True:
        choix_douzaine = input("choisissez 1, 2 ou 3 pour votre douzaine : ")
        try:
            choix_douzaine = int(choix_douzaine)
            if choix_douzaine in [1, 2, 3]:
                return choix_douzaine
            else:
                print("choisissez une option valide")
        except ValueError:
            print("erreur")


def demander_couleur():
    while True:
        choix_couleur = input("choisissez votre couleur : ").strip().lower()
        if choix_couleur in ["rouge", "noir"]:
            return choix_couleur
        else:
            print("choisissez soit rouge soit noir")


def demander_numero():
    while True:
        choix_numero = input("choisissez votre numéro : ")
        try:
            choix_numero = int(choix_numero)
            if choix_numero >= 0 and choix_numero <= 36:
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


def jouer():
    solde = charger_solde()

    while True:
        menu = input("jouer ou stop : ").lower().strip()
        if menu == "jouer":
            if not peut_jouer(solde):
                print("solde insuffisant")
                continue
            print("solde disponible : ", solde)
            choix_couleur = None
            choix_numero = None
            paire_impair = None
            manque_passe = None
            choix_douzaine = None
            options = [
                "couleur",
                "numéro",
                "pair",
                "impair",
                "manque",
                "passe",
                "douzaine",
                "lancer",
            ]

            while True:
                if len(options) == 1:
                    break
                if not peut_jouer(solde):
                    print("solde insuffisant pour d'autre paris lancement de la bille")
                    break
                choix = demander_pari(options)
                if choix == "couleur":
                    choix_couleur = demander_couleur()
                    mise_couleur = demander_mise(solde)
                    solde -= mise_couleur
                    options.remove("couleur")
                elif choix == "numéro":
                    choix_numero = demander_numero()
                    mise_numero = demander_mise(solde)
                    solde -= mise_numero
                    options.remove("numéro")
                elif choix == "pair" or choix == "impair":
                    paire_impair = choix
                    mise_parite = demander_mise(solde)
                    solde -= mise_parite
                    options.remove("pair")
                    options.remove("impair")
                elif choix == "manque" or choix == "passe":
                    manque_passe = choix
                    mise_moitie = demander_mise(solde)
                    solde -= mise_moitie
                    options.remove("manque")
                    options.remove("passe")
                elif choix == "douzaine":
                    choix_douzaine = demander_douzaine()
                    mise_douzaine = demander_mise(solde)
                    solde -= mise_douzaine
                    options.remove("douzaine")
                elif choix == "lancer":
                    break

            numero = random.randint(0, 36)

            if numero in NUMEROS_ROUGES:
                couleur = "rouge"
            elif numero == 0:
                couleur = "vert"
            else:
                couleur = "noir"

            gain_total = 0
            print(numero, couleur)

            if choix_couleur is not None:
                if choix_couleur == couleur:
                    print("couleur : gagné")
                    gain = mise_couleur * 2
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print("couleur : perdu")

            if choix_numero is not None:
                if choix_numero == numero:
                    print("numéro : gagné")
                    gain = mise_numero * 36
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print("numéro : perdu")

            if numero == 0:
                parite = 0
            elif numero % 2 == 0:
                parite = "pair"
            else:
                parite = "impair"

            if paire_impair is not None:
                if paire_impair == parite:
                    print("parité : gagné")
                    gain = mise_parite * 2
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print("parité : perdu")

            if numero == 0:
                moitie = 0
            elif numero >= 1 and numero <= 18:
                moitie = "manque"
            else:
                moitie = "passe"

            if manque_passe is not None:
                if manque_passe == moitie:
                    print(manque_passe, ": gagné")
                    gain = mise_moitie * 2
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print(manque_passe, ": perdu")

            if numero == 0:
                douzaine = 0
            elif numero >= 1 and numero <= 12:
                douzaine = 1
            elif numero >= 13 and numero <= 24:
                douzaine = 2
            else:
                douzaine = 3

            if choix_douzaine is not None:
                if choix_douzaine == douzaine:
                    print("douzaine", choix_douzaine, ": gagné")
                    gain = mise_douzaine * 3
                    solde += gain
                    gain_total += gain
                    print("gain gagné : ", gain)
                else:
                    print("douzaine", choix_douzaine, ": perdu")

            print("gain total gagné : ", gain_total)
            sauvegarder_solde(solde)
        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
