import json

FICHIER = "portefeuille.json"
SOLDE_DEPART = 1000


def charger_solde():
    try:
        with open(FICHIER, "r") as f:
            donnees = json.load(f)
            return donnees["solde"]
    except FileNotFoundError:
        return SOLDE_DEPART
    except json.JSONDecodeError:
        return SOLDE_DEPART


def demander_mise(solde):
    while True:
        reponse = input("votre mise : ")
        try:
            reponse = int(reponse)
            if reponse >= 1 and reponse <= solde:
                return reponse
            else:
                print("mise entre 1 et ", solde)
        except ValueError:
            print("erreur")


def peut_jouer(solde):
    return solde >= 1  # renvoie un True or False directement


def sauvegarder_solde(solde):
    with open(FICHIER, "w") as f:
        json.dump({"solde": solde}, f)
