import random

COULEURS = ["cœur", "carreau", "trèfle", "pique"]

VALEURS = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi"]

def créer_paquet():
    paquet = []

    for couleur in COULEURS:
        for valeur in VALEURS:
            carte = {"couleur": couleur, "valeur": valeur}
            paquet.append(carte)

    random.shuffle(paquet)
    return paquet
