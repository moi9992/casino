from cartes import créer_paquet
from poker_outils import afficher_main
from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

GAIN = {"joueur": 2, "banquier": 1.95, "égalité": 9}


def demander_pari():
    while True:
        choix = (
            (input("Voulez vous miser sur le joueur, le banquier ou une égalité : "))
            .lower()
            .strip()
        )
        if choix in ["joueur", "banquier", "égalité"]:
            return choix
        else:
            print("choisissez une option valide")


def distribuer():
    paquet = créer_paquet()

    main_joueur = []
    main_banquier = []

    for i in range(2):
        main_banquier.append(paquet.pop())
        main_joueur.append(paquet.pop())

    naturel = False

    if valeur_main(main_joueur) in [8, 9] or valeur_main(main_banquier) in [
        8,
        9,
    ]:
        naturel = True

    troisieme_joueur = None

    if naturel == False and valeur_main(main_joueur) <= 5:
        main_joueur.append(paquet.pop())
        troisieme_joueur = valeur_carte(main_joueur[-1])

    if (
        naturel == False
        and troisieme_joueur is None
        and valeur_main(main_banquier) <= 5
    ):
        main_banquier.append(paquet.pop())

    elif naturel == False and troisieme_joueur is not None:
        if valeur_main(main_banquier) <= 2:
            main_banquier.append(paquet.pop())
        elif valeur_main(main_banquier) == 3:
            if troisieme_joueur != 8:
                main_banquier.append(paquet.pop())
        elif valeur_main(main_banquier) == 4:
            if troisieme_joueur >= 2 and troisieme_joueur <= 7:
                main_banquier.append(paquet.pop())
        elif valeur_main(main_banquier) == 5:
            if troisieme_joueur >= 4 and troisieme_joueur <= 7:
                main_banquier.append(paquet.pop())
        elif valeur_main(main_banquier) == 6 and (
            troisieme_joueur == 6 or troisieme_joueur == 7
        ):
            main_banquier.append(paquet.pop())
    return main_joueur, main_banquier


def trouver_resultat(main_joueur, main_banquier):
    if valeur_main(main_joueur) > valeur_main(main_banquier):
        resultat = "joueur"
    elif valeur_main(main_joueur) < valeur_main(main_banquier):
        resultat = "banquier"
    else:
        resultat = "égalité"
    return resultat


def valeur_carte(carte):
    if carte["valeur"] in ["10", "Valet", "Dame", "Roi"]:
        return 0
    elif carte["valeur"] in ["As"]:
        return 1
    else:
        return int(carte["valeur"])


def valeur_main(main):
    total = 0
    for carte in main:
        total += valeur_carte(carte)
    return total % 10


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
            pari = demander_pari()
            main_joueur, main_banquier = distribuer()

            print("joueur :", valeur_main(main_joueur))
            afficher_main(main_joueur)
            print("banquier :", valeur_main(main_banquier))
            afficher_main(main_banquier)

            resultat = trouver_resultat(main_joueur, main_banquier)

            if pari == resultat:
                gain = round(mise * GAIN[pari], 2)
                solde += gain
                print("pari : gagné\ngain gagné : ", gain)
            elif resultat == "égalité":
                solde += mise
                print("égalité : mise rendu")
            else:
                print("pari : perdu")

            sauvegarder_solde(solde)
        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
