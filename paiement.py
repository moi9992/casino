from datetime import date

PACKS = {"petit joueur": 10, "habitué": 50, "flambeur": 100, "whale": 500}
MONTANT_MAX = 999_999_999
MONTANT_MIN = 1_000


def verifier_cvc(cvc):
    return cvc.isdigit() and len(cvc) == 3


def verifier_expiration(expiration):
    if len(expiration) != 5 or expiration[2] != "/":
        return False
    mois, annee = expiration.split("/")
    if not mois.isdigit() or not annee.isdigit():
        return False
    mois = int(mois)
    annee = int(annee)
    if mois < 1 or mois > 12:
        return False
    aujourdhui = date.today()
    annee += 2000
    if annee < aujourdhui.year:
        return False
    return not (
        mois < aujourdhui.month and annee == aujourdhui.year
    )  # expirée si c'est l'année en cours mais un mois déjà passé


def verifier_luhn(numero):
    if not numero.isdigit() or len(numero) != 16:
        return False
    chiffres = numero[::-1]
    total = 0
    for i in range(len(chiffres)):
        chiffre = int(chiffres[i])
        if i % 2 == 1:
            chiffre = chiffre * 2
            if chiffre > 9:
                chiffre -= 9
        total += chiffre
    return total % 10 == 0
