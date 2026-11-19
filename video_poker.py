from cartes import créer_paquet
from poker_outils import afficher_main, evaluer_main, rang
from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

GAIN = {
    "quinte flush royal": 250,
    "quinte flush": 50,
    "carré": 25,
    "full": 9,
    "couleur": 6,
    "quinte": 4,
    "brelan": 3,
    "double paire": 2,
    "paire": 1,
    "rien": 0,
}


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
            paquet = créer_paquet()

            main_joueur = []

            for i in range(5):
                main_joueur.append(paquet.pop())

            afficher_main(main_joueur)

            choix = input("quelles cartes gardez-vous ou tout ? : ").strip().split()

            for i in range(5):
                if (str(i + 1)) not in choix and "tout" not in choix:
                    main_joueur[i] = paquet.pop()

            afficher_main(main_joueur)

            combinaison = evaluer_main(main_joueur)

            if combinaison == "paire":
                paire_haute = False
                valeurs = []
                for carte in main_joueur:
                    valeurs.append(carte["valeur"])
                for valeur in valeurs:
                    if rang(valeur) >= 11 and valeurs.count(valeur) == 2:
                        paire_haute = True
                if paire_haute == False:
                    combinaison = "rien"

            print(combinaison)
            gain = mise * GAIN[combinaison]
            solde += gain

            print("gain gagné : ", gain)
            sauvegarder_solde(solde)

        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
