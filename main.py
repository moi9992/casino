import baccarat
import bingo
import blackjack
import caribbean_stud
import craps
import crash
import keno
import machine_a_sous
import mine
import plus_ou_moins
import roue_fortune
import roulette
import sic_bo
import video_poker
from portefeuille import charger_solde

JEUX = {
    "baccarat": baccarat.jouer,
    "bingo": bingo.jouer,
    "blackjack": blackjack.jouer,
    "caribbean stud": caribbean_stud.jouer,
    "craps": craps.jouer,
    "crash": crash.jouer,
    "keno": keno.jouer,
    "machine a sous": machine_a_sous.jouer,
    "mine": mine.jouer,
    "plus ou moins": plus_ou_moins.jouer,
    "roue de la fortune": roue_fortune.jouer,
    "roulette": roulette.jouer,
    "sic bo": sic_bo.jouer,
    "video poker": video_poker.jouer,
}


def demander_jeux():
    while True:
        print("Jeux disponible : ")
        for jeu in JEUX:
            print("-", jeu)
        choix = (input("choisissez votre jeu ou quitter : ")).strip().lower()
        if choix in JEUX or choix == "quitter":
            return choix
        else:
            print("choisissez une option valide")


print("bienvenu sur le casino des casino")
while True:
    solde = charger_solde()
    print()
    print("vous avez : ", solde, "solde disponible")
    choix = demander_jeux()
    if choix == "quitter":
        break
    else:
        JEUX[choix]()
