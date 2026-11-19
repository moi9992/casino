from cartes import créer_paquet
from poker_outils import afficher_main, evaluer_main, rang
from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

COMBINAISON = {
    "rien": 1,
    "paire": 2,
    "double paire": 3,
    "brelan": 4,
    "quinte": 5,
    "couleur": 6,
    "full": 7,
    "carré": 8,
    "quinte flush": 9,
    "quinte flush royal": 10,
}

GAIN = {
    "rien": 2,
    "paire": 2,
    "double paire": 3,
    "brelan": 4,
    "quinte": 5,
    "couleur": 6,
    "full": 8,
    "carré": 21,
    "quinte flush": 51,
    "quinte flush royal": 101,
}


def croupier_qualifie(main):
    if evaluer_main(main) != "rien":
        return True
    valeurs = []
    for carte in main:
        valeurs.append(carte["valeur"])
    return (
        "As" in valeurs and "Roi" in valeurs
    )  # renvoie directement True ou False : vrai seulement si l'As ET le Roi sont dans la main


def comparer_mains(main_joueur, main_croupier):
    score_joueur = COMBINAISON[evaluer_main(main_joueur)]
    score_croupier = COMBINAISON[evaluer_main(main_croupier)]
    if score_joueur > score_croupier:
        return "joueur"
    elif score_croupier > score_joueur:
        return "croupier"
    elif score_joueur == score_croupier:
        if rangs_tries(main_joueur) > rangs_tries(main_croupier):
            return "joueur"
        elif rangs_tries(main_croupier) > rangs_tries(main_joueur):
            return "croupier"
        elif rangs_tries(main_croupier) == rangs_tries(main_joueur):
            return "egalite"


def rangs_tries(main):
    valeur = []
    for carte in main:
        valeur.append(rang(carte["valeur"]))
    valeur.sort(reverse=True)
    ordre = []
    for carre in valeur:
        if valeur.count(carre) == 4:
            ordre.append(carre)
    for brelan in valeur:
        if valeur.count(brelan) == 3:
            ordre.append(brelan)
    for paire in valeur:
        if valeur.count(paire) == 2:
            ordre.append(paire)
    for unique in valeur:
        if valeur.count(unique) == 1:
            ordre.append(unique)
    if ordre == [14, 5, 4, 3, 2]:
        ordre = [5, 4, 3, 2, 1]
    return ordre


def jouer():
    solde = charger_solde()

    while True:
        menu = input("jouer ou stop : ").strip().lower()
        if menu == "jouer":
            if not peut_jouer(solde // 3):
                print("solde insuffisant")
                continue
            print("solde disponible : ", solde)
            mise = demander_mise(solde // 3)
            solde = solde - mise
            paquet = créer_paquet()

            main_joueur = []
            main_croupier = []

            for i in range(5):
                main_joueur.append(paquet.pop())
                main_croupier.append(paquet.pop())

            print("main du joueur : ")
            afficher_main(main_joueur)
            print("main du croupier : ")
            afficher_main([main_croupier[0]])

            while True:
                reponse = input("jouer ou coucher : ").strip().lower()

                if reponse == "jouer" or reponse == "coucher":
                    break

            if reponse == "coucher":
                print("perdu")
                sauvegarder_solde(solde)
                continue

            relance = mise * 2
            solde -= relance

            print("main complète du croupier")
            afficher_main(main_croupier)

            if not croupier_qualifie(main_croupier):
                print("joueur : gagne")
                gain = mise * 2 + relance
                solde += gain
                print("gain gagné : ", gain)
                sauvegarder_solde(solde)
                continue

            resultat = comparer_mains(main_joueur, main_croupier)
            if resultat == "joueur":
                print("joueur : gagne")
                gain = mise * 2 + relance * GAIN[evaluer_main(main_joueur)]
            elif resultat == "croupier":
                print("croupier : gagne")
                gain = 0
            else:
                print("égalité")
                gain = mise + relance

            solde += gain
            print("gain gagné : ", gain)

            sauvegarder_solde(solde)
        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
