import random

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

COTE_MAX = {
    4: 3,
    5: 4,
    6: 5,
    8: 5,
    9: 4,
    10: 3,
}

PAIEMENT_COTE = {4: 2, 5: 1.5, 6: 1.2, 8: 1.2, 9: 1.5, 10: 2}

PAIEMENT_COTE_NE_PAS_PASSER = {
    4: 0.5,
    5: 2 / 3,
    6: 5 / 6,
    8: 5 / 6,
    9: 2 / 3,
    10: 0.5,
}

COTE_MAX_NE_PAS_PASSER = 6


def demander_camp():
    while True:
        reponse = input("passer ou ne pas passer : ").strip().lower()
        if reponse == "passer" or reponse == "ne pas passer":
            return reponse
        else:
            print("choisissez une option valide")


def demander_cote(mise, point, solde, camp):
    if camp == "passer":
        cote_max = mise * COTE_MAX[point]
    else:
        cote_max = mise * COTE_MAX_NE_PAS_PASSER
    cote_max = min(solde, cote_max)
    while True:
        reponse = input(
            f"choisissez la valeur de votre cote allant de 0 à {cote_max} : "
        )
        try:
            reponse = int(reponse)
            if reponse >= 0 and reponse <= cote_max:
                return reponse
            else:
                print("choisissez une option valide")
        except ValueError:
            print("erreur")


def lancer_des():
    dee_tirer = []

    for i in range(2):
        tirage = random.randint(1, 6)
        dee_tirer.append(tirage)

    total = sum(dee_tirer)

    return total


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
            camp = demander_camp()
            cote = 0

            total = lancer_des()
            print(total)
            if total == 7 or total == 11:
                resultat = "gagne"
            elif total == 2 or total == 3:
                resultat = "perdu"
            elif total == 12:
                resultat = "douze"
            else:
                point = total
                print("point : ", point)
                cote = demander_cote(mise, point, solde, camp)
                solde -= cote
                while True:
                    total = lancer_des()
                    print(total)
                    if total == point:
                        resultat = "gagne"
                        break
                    elif total == 7:
                        resultat = "perdu"
                        break

            if camp == "passer" and resultat == "douze":
                resultat = "perdu"
            elif camp == "ne pas passer":
                if resultat == "douze":
                    resultat = "egalite"
                elif resultat == "gagne":
                    resultat = "perdu"
                elif resultat == "perdu":
                    resultat = "gagne"

            if resultat == "gagne":
                gain = mise * 2
                solde += gain
                print("gain gagné : ", gain)
                if cote > 0:
                    if camp == "passer":
                        paiement = PAIEMENT_COTE[point]
                    else:
                        paiement = PAIEMENT_COTE_NE_PAS_PASSER[point]
                    gain_cote = round(cote * paiement, 2)
                    solde += cote + gain_cote
                    print("gain de la cote : ", gain_cote)
            elif resultat == "egalite":
                solde += mise
                print("égalité mise rendue")
            else:
                print("perdu")

            sauvegarder_solde(solde)

        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
