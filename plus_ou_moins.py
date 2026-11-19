from cartes import créer_paquet
from poker_outils import afficher_main, rang
from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde


def bon_pari(carte_actuelle, nouvelle_carte, pari):
    rang_actuel = rang(carte_actuelle["valeur"])
    rang_nouveau = rang(nouvelle_carte["valeur"])
    return (
        (pari == "haut" and rang_actuel < rang_nouveau)
        or (pari == "bas" and rang_actuel > rang_nouveau)
    )  # renvoie directement True ou False : gagné si "haut" et la nouvelle carte est plus haute, ou si "bas" et elle est plus basse


def calculer_multiplicateur(carte_actuelle, pari):
    rang_actuel = rang(carte_actuelle["valeur"])
    if pari == "haut":
        rangs_gagnants = 14 - rang_actuel
    else:
        rangs_gagnants = rang_actuel - 2
    if rangs_gagnants == 0:
        return 0
    return round(13 / rangs_gagnants, 2)


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
            carte_actuelle = paquet.pop()

            bonne_reponse = 0
            gain = mise

            while True:
                afficher_main([carte_actuelle])

                while True:
                    reponse = input("haut ou bas : ").lower().strip()

                    if reponse == "haut" or reponse == "bas":
                        multiplicateur = calculer_multiplicateur(
                            carte_actuelle, reponse
                        )
                        if multiplicateur == 0:
                            print("pari impossible")
                        else:
                            break

                nouvelle_carte = paquet.pop()

                afficher_main([nouvelle_carte])

                if bon_pari(carte_actuelle, nouvelle_carte, reponse):
                    print("gagné")
                    bonne_reponse += 1
                    carte_actuelle = nouvelle_carte
                    gain = round((gain * multiplicateur), 2)
                    print(gain)

                    while True:
                        choix = input("continuer ou encaisser : ").lower().strip()
                        if choix == "continuer":
                            break
                        elif choix == "encaisser":
                            print("bonne réponse : ", bonne_reponse)
                            break

                    if choix == "encaisser":
                        solde += gain
                        break

                else:
                    print("perdu")
                    break

            sauvegarder_solde(solde)

        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
