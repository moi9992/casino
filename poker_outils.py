def afficher_main(main):
    numero = 1

    for carte in main:
        print(numero, "-", carte["valeur"], "de", carte["couleur"])
        numero += 1


def evaluer_main(main):
    nombres = []
    valeurs = []
    couleurs = []
    rangs = []
    for carte in main:
        couleurs.append(carte["couleur"])
        valeurs.append(carte["valeur"])

    couleur_sortie = couleurs.count(couleurs[0])

    if couleur_sortie == 5:
        est_couleur = True
    else:
        est_couleur = False

    for valeur in valeurs:
        nombres.append(valeurs.count(valeur))
        rangs.append(rang(valeur))

    rangs.sort()

    brelan = 3 in nombres
    carre = 4 in nombres
    nb_paire = nombres.count(2)
    quinte = (
        nombres.count(1) == 5 and rangs[4] - rangs[0] == 4 or rangs == [2, 3, 4, 5, 14]
    )

    if quinte == True and est_couleur == True and rangs[0] == 10:
        return "quinte flush royal"
    elif quinte == True and est_couleur == True:
        return "quinte flush"
    elif carre == True:
        return "carré"
    elif brelan == True and nb_paire == 2:
        return "full"
    elif est_couleur == True:
        return "couleur"
    elif quinte == True:
        return "quinte"
    elif brelan == True:
        return "brelan"
    elif nb_paire == 4:
        return "double paire"
    elif nb_paire == 2:
        return "paire"
    else:
        return "rien"


def rang(valeur):
    if valeur == "Valet":
        return 11
    elif valeur == "Dame":
        return 12
    elif valeur == "Roi":
        return 13
    elif valeur == "As":
        return 14
    else:
        return int(valeur)
