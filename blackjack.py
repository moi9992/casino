from cartes import créer_paquet
from poker_outils import afficher_main
from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

GAIN = {"blackjack": 2.5, "gagné": 2, "égalité": 1, "perdu": 0}


def distribuer(paquet):
    main_joueur = []
    main_croupier = []

    for i in range(2):
        main_joueur.append(paquet.pop())
        main_croupier.append(paquet.pop())
    return main_joueur, main_croupier


def jouer_croupier(main_croupier, paquet):
    while points_main(main_croupier) < 17:
        main_croupier.append(paquet.pop())


def points_carte(carte):
    if carte["valeur"] in ["Valet", "Dame", "Roi"]:
        return 10
    elif carte["valeur"] in ["As"]:
        return 11
    else:
        return int(carte["valeur"])


def points_main(main):
    total = 0
    nb_as = 0
    for carte in main:
        total += points_carte(carte)
        if carte["valeur"] == "As":
            nb_as += 1
    while total > 21 and nb_as > 0:
        total -= 10
        nb_as -= 1
    return total


def options_possibles(main):
    options = ["hit", "stop"]
    if len(main) == 2:
        options.append("doubler")
        if main[0]["valeur"] == main[1]["valeur"]:
            options.append("split")
    return options


def resultat_main(main, main_croupier):
    if points_main(main) > 21:
        resultat = "perdu"
    elif points_main(main_croupier) > 21 or points_main(main) > points_main(
        main_croupier
    ):
        resultat = "gagné"
    elif points_main(main) == points_main(main_croupier):
        resultat = "égalité"
    else:
        resultat = "perdu"
    return resultat


def verifier_blackjacks(main_joueur, main_croupier):
    if points_main(main_joueur) == 21 and points_main(main_croupier) == 21:
        resultat = "égalité"
    elif points_main(main_joueur) == 21:
        resultat = "blackjack"
    elif points_main(main_croupier) == 21:
        resultat = "perdu"
    else:
        resultat = None
    return resultat


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
            paquet = créer_paquet()
            partie_fini = False

            main_joueur, main_croupier = distribuer(paquet)

            mains = [main_joueur]
            mises = [mise]
            as_splittes = [False]

            resultat = verifier_blackjacks(main_joueur, main_croupier)
            if resultat is not None:
                partie_fini = True
                print(resultat)
            else:
                i = 0
                while i < len(mains):
                    main = mains[i]
                    while True:
                        print("main du joueur :", (points_main(main)))
                        afficher_main(main)
                        print("main du croupier ")
                        afficher_main([main_croupier[0]])
                        if as_splittes[i] == True:
                            print("As splittés : une seule carte")
                            break

                        options = options_possibles(main)
                        reponse = input(", ".join(options) + " : ").strip().lower()

                        if reponse == "hit":
                            main.append(paquet.pop())

                            if points_main(main) > 21:
                                print("perdu")
                                resultat = "perdu"
                                break

                        if reponse == "doubler" and len(main) == 2:
                            if solde < mises[i]:
                                print("solde insuffisant pour doubler")
                            else:
                                solde -= mises[i]
                                mises[i] *= 2
                                main.append(paquet.pop())
                                afficher_main(main)
                                print("main du joueur : ", points_main(main))
                                if points_main(main) > 21:
                                    print("perdu")
                                    resultat = "perdu"
                                    break
                                break

                        if (
                            reponse == "split"
                            and len(main) == 2
                            and main[0]["valeur"] == main[1]["valeur"]
                        ):
                            if len(mains) == 4:
                                print("maximum de 4 mains")
                            elif solde < mises[i]:
                                print("solde insuffisant pour split")
                            else:
                                solde -= mises[i]
                                nouvelle_main = [main.pop()]
                                main.append(paquet.pop())
                                nouvelle_main.append(paquet.pop())
                                mains.insert(i + 1, nouvelle_main)
                                mises.insert(i + 1, mises[i])
                                as_splittes.insert(i + 1, False)
                                if main[0]["valeur"] == "As":
                                    as_splittes[i] = True
                                    as_splittes[i + 1] = True

                        if reponse == "stop":
                            print("main du joueur :", (points_main(main)))
                            break

                    i += 1
            if partie_fini == False:
                jouer_croupier(main_croupier, paquet)
                print("main du croupier :", (points_main(main_croupier)))
                afficher_main(main_croupier)
                for i in range(len(mains)):
                    main = mains[i]
                    print("main : ", i + 1, points_main(main))
                    resultat = resultat_main(main, main_croupier)
                    print(resultat)

                    gain = round(mises[i] * GAIN[resultat], 2)
                    solde += gain
                    print("gain gagné : ", gain)

            else:
                gain = round(mise * GAIN[resultat], 2)
                solde += gain
                print("gain gagné : ", gain)

            sauvegarder_solde(solde)
        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
