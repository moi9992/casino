from cartes import créer_paquet
from poker_outils import afficher_main
from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

GAIN = {"blackjack": 2.5, "gagné": 2, "égalité": 1, "perdu": 0}


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

            main_joueur = []
            main_croupier = []
            partie_fini = False

            for i in range(2):
                main_joueur.append(paquet.pop())
                main_croupier.append(paquet.pop())

            mains = [main_joueur]
            mises = [mise]
            as_splittes = [False]

            if points_main(main_joueur) == 21 and points_main(main_croupier) == 21:
                partie_fini = True
                print("DOUBLE BLACKJACK, égalité")
                resultat = "égalité"
            elif points_main(main_joueur) == 21:
                partie_fini = True
                print("BLACKJACK, tu as gagné")
                resultat = "blackjack"
            elif points_main(main_croupier) == 21:
                partie_fini = True
                print("BLACKJACK du croupier, tu as perdu")
                resultat = "perdu"
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
                        options = ["hit", "stop"]
                        if len(main) == 2:
                            options.append("doubler")
                            if main[0]["valeur"] == main[1]["valeur"]:
                                options.append("split")
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
                while points_main(main_croupier) < 17:
                    main_croupier.append(paquet.pop())
                print("main du croupier :", (points_main(main_croupier)))
                afficher_main(main_croupier)
                for i in range(len(mains)):
                    main = mains[i]
                    print("main : ", i + 1, points_main(main))
                    if points_main(main) > 21:
                        print("perdu")
                        resultat = "perdu"
                    elif points_main(main_croupier) > 21 or points_main(
                        main
                    ) > points_main(main_croupier):
                        print("gagné")
                        resultat = "gagné"
                    elif points_main(main) == points_main(main_croupier):
                        print("égalité")
                        resultat = "égalité"
                    else:
                        print("perdu")
                        resultat = "perdu"

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
