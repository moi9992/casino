import random

from portefeuille import charger_solde, demander_mise, peut_jouer, sauvegarder_solde

TAILLE = 5
NB_BOMBES = 3


def afficher_grille(grille):
    for ligne in grille:
        print(" ".join(ligne))


def calculer_multiplicateur(cases_trouvees):
    cases_restantes = TAILLE * TAILLE - cases_trouvees
    cases_sures = cases_restantes - NB_BOMBES
    return round((cases_restantes / cases_sures), 2)


def creer_grille(contenu):
    grille = []

    for _ in range(TAILLE):
        ligne = [contenu] * TAILLE
        grille.append(ligne)

    return grille


def demander_position(message):
    while True:
        reponse = input(message)
        try:
            reponse = int(reponse)
            if reponse in range(1, TAILLE + 1):
                return reponse - 1
            else:
                print("choisissez une option valide")
        except ValueError:
            print("erreur")


def placer_bombe(grille):
    bombe_poser = 0
    while bombe_poser < NB_BOMBES:
        ligne = random.randint(0, TAILLE - 1)
        colonne = random.randint(0, TAILLE - 1)
        if grille[ligne][colonne] != "B":
            grille[ligne][colonne] = "B"
            bombe_poser += 1


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
            grille = creer_grille("?")
            bombe = creer_grille("V")
            placer_bombe(bombe)
            afficher_grille(grille)

            cases_trouvees = 0
            gain = mise
            while True:
                ligne = demander_position("choisissez votre ligne : ")
                colonne = demander_position("choisissez votre colonne : ")

                if grille[ligne][colonne] == "✅":
                    print("choisissez une case non choisit")
                    continue

                if "B" == bombe[ligne][colonne]:
                    print("perdu")
                    afficher_grille(bombe)
                    break
                else:
                    grille[ligne][colonne] = "✅"
                    gain = round(gain * calculer_multiplicateur(cases_trouvees), 2)
                    print("gain en jeu : ", gain)
                    cases_trouvees += 1

                    if cases_trouvees == TAILLE * TAILLE - NB_BOMBES:
                        print("gagné")
                        solde += gain
                        break

                    afficher_grille(grille)
                    while True:
                        reponse = input("continuer ou encaisser : ").strip().lower()

                        if reponse == "continuer":
                            break
                        elif reponse == "encaisser":
                            print("cases trouver : ", cases_trouvees)
                            solde += gain
                            break
                if reponse == "encaisser":
                    break

            sauvegarder_solde(solde)

        elif menu == "stop":
            break


if __name__ == "__main__":
    jouer()
