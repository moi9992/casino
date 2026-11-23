import os
import secrets

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

import baccarat
import blackjack
import bingo
import caribbean_stud
import craps
import crash
import keno
import machine_a_sous
import mine
import roue_fortune
import roulette
import sic_bo
import video_poker
import plus_ou_moins
from cartes import créer_paquet
from portefeuille import charger_solde, sauvegarder_solde

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

parties = {}


@app.route("/")
def accueil():
    solde = charger_solde()
    return render_template("accueil.html", solde=solde)


@app.route("/plus-ou-moins", methods=["GET", "POST"])
def page_plus_ou_moins():
    message = session.pop("message", None)
    ancienne_carte = session.pop("ancienne_carte", None)
    carte_perdante = session.pop("carte_perdante", None)
    solde = charger_solde()
    partie_id = session.get("partie_plus_ou_moins")
    partie = parties.get(partie_id)
    if request.method == "POST":
        if request.form.get("action") == "commencer":
            try:
                mise = int(request.form["mise"])
                if mise >= 1 and mise <= solde:
                    solde -= mise
                    sauvegarder_solde(solde)
                    partie_id = secrets.token_hex(16)
                    parties[partie_id] = {
                        "carte_actuelle": créer_paquet().pop(),
                        "gain": mise,
                    }
                    session["partie_plus_ou_moins"] = partie_id
                else:
                    message = "mise invalide"
            except ValueError:
                message = "mise invalide"
        elif request.form.get("action") == "encaisser" and partie is not None:
            solde += partie["gain"]
            sauvegarder_solde(solde)
            message = "encaissé"
            session.pop("partie_plus_ou_moins")
            parties.pop(partie_id)
        elif "pari" in request.form and partie is not None:
            pari = request.form["pari"]
            multiplicateur = plus_ou_moins.calculer_multiplicateur(
                partie["carte_actuelle"], pari
            )
            if multiplicateur == 0:
                message = "pari impossible"
            else:
                nouvelle_carte = créer_paquet().pop()
                if plus_ou_moins.bon_pari(
                    partie["carte_actuelle"], nouvelle_carte, pari
                ):
                    message = "gagné"
                    partie["gain"] = round(
                        partie["gain"] * multiplicateur,
                        2,
                    )
                else:
                    message = "perdu"
                    session["carte_perdante"] = nouvelle_carte
                    session.pop("partie_plus_ou_moins")
                    parties.pop(partie_id)
                ancienne_carte = partie["carte_actuelle"]
                partie["carte_actuelle"] = nouvelle_carte
        session["message"] = message
        session["ancienne_carte"] = ancienne_carte
        return redirect(url_for("page_plus_ou_moins"))
    return render_template(
        "plus_ou_moins.html",
        solde=solde,
        message=message,
        ancienne_carte=ancienne_carte,
        carte_perdante=carte_perdante,
        partie=partie,
    )


@app.route("/machine-a-sous", methods=["GET", "POST"])
def page_machine_a_sous():
    message = session.pop("message", None)
    solde = charger_solde()
    tirage = session.pop("tirage", None)
    if request.method == "POST":
        try:
            mise = int(request.form["mise"])
            if mise >= 1 and mise <= solde:
                solde -= mise
                tirage = machine_a_sous.tirer_rouleaux()
                gain = mise * machine_a_sous.calculer_multiplicateur(tirage)
                solde += gain
                sauvegarder_solde(solde)
                message = f"gain : {gain}"
            else:
                message = "mise invalide"
        except ValueError:
            message = "mise invalide"
        session["message"] = message
        session["tirage"] = tirage
        return redirect(url_for("page_machine_a_sous"))
    return render_template(
        "machine_a_sous.html", solde=solde, tirage=tirage, message=message
    )


@app.route("/roue-de-la-fortune", methods=["GET", "POST"])
def page_roue_de_la_fortune():
    message = session.pop("message", None)
    solde = charger_solde()
    tirage = session.pop("tirage", None)
    if request.method == "POST":
        try:
            mise = int(request.form["mise"])
            choix = request.form["choix"]
            if mise >= 1 and mise <= solde:
                solde -= mise
                tirage = roue_fortune.tourner_roue()
                if choix == tirage:
                    gain = mise + mise * roue_fortune.GAIN[choix]
                else:
                    gain = 0
                solde += gain
                sauvegarder_solde(solde)
                message = f"gain : {gain}"
            else:
                message = "mise invalide"
        except ValueError:
            message = "mise invalide"
        session["message"] = message
        session["tirage"] = tirage
        return redirect(url_for("page_roue_de_la_fortune"))
    return render_template(
        "roue_fortune.html", solde=solde, tirage=tirage, message=message
    )


@app.route("/crash", methods=["GET", "POST"])
def page_crash():
    message = session.pop("message", None)
    solde = charger_solde()
    crash_tire = session.pop("crash_tire", None)
    if request.method == "POST":
        try:
            mise = int(request.form["mise"])
            objectif = request.form["objectif"].replace(",", ".")
            objectif = float(objectif)
            if mise >= 1 and mise <= solde and crash.objectif_valide(objectif):
                solde -= mise
                crash_tire = crash.tirer_crash()
                if objectif <= crash_tire:
                    gain = round(mise * objectif, 2)
                else:
                    gain = 0
                solde += gain
                sauvegarder_solde(solde)
                message = f"gain : {gain}"
            else:
                message = "objectif invalide"
        except ValueError:
            message = "objectif invalide"
        session["message"] = message
        session["crash_tire"] = crash_tire
        return redirect(url_for("page_crash"))
    return render_template(
        "crash.html", solde=solde, crash_tire=crash_tire, message=message
    )


@app.route("/keno", methods=["GET", "POST"])
def page_keno():
    message = session.pop("message", None)
    solde = charger_solde()
    tirage = session.pop("tirage", None)
    if request.method == "POST":
        try:
            mise = int(request.form["mise"])
            numeros = keno.lire_numeros(request.form["numeros"])
            if mise >= 1 and mise <= solde and numeros is not None:
                solde -= mise
                tirage = keno.tirer_numeros()
                bons_numero = keno.compter_bons(numeros, tirage)
                gain = mise * keno.GAIN[bons_numero]
                solde += gain
                sauvegarder_solde(solde)
                message = f"bon numero : {bons_numero}, gain : {gain}"
            else:
                message = "choisissez une option valide"
        except ValueError:
            message = "choisissez une option valide"
        session["message"] = message
        session["tirage"] = tirage
        return redirect(url_for("page_keno"))
    return render_template("keno.html", solde=solde, tirage=tirage, message=message)


@app.route("/baccarat", methods=["GET", "POST"])
def page_baccarat():
    message = session.pop("message", None)
    main_joueur = session.pop("main_joueur", None)
    main_banquier = session.pop("main_banquier", None)
    solde = charger_solde()
    if request.method == "POST":
        try:
            mise = int(request.form["mise"])
            pari = request.form["pari"]
            if mise >= 1 and mise <= solde and pari in baccarat.GAIN:
                solde -= mise
                main_joueur, main_banquier = baccarat.distribuer()
                resultat = baccarat.trouver_resultat(main_joueur, main_banquier)
                if pari == resultat:
                    gain = round(mise * baccarat.GAIN[pari], 2)
                    solde += gain
                    message = f"pari : gagné, gain gagné :  {gain}"
                elif resultat == "égalité":
                    solde += mise
                    message = "égalité : mise rendu"
                else:
                    message = "pari : perdu"
                sauvegarder_solde(solde)
            else:
                message = "choisissez une option valide"
        except ValueError:
            message = "choisissez une option valide"
        session["message"] = message
        session["main_joueur"] = main_joueur
        session["main_banquier"] = main_banquier
        return redirect(url_for("page_baccarat"))
    return render_template(
        "baccarat.html",
        solde=solde,
        main_joueur=main_joueur,
        main_banquier=main_banquier,
        message=message,
    )


@app.route("/sic-bo", methods=["GET", "POST"])
def page_sic_bo():
    message = session.pop("message", None)
    dee_tirer = session.pop("dee_tirer", None)
    solde = charger_solde()
    if request.method == "POST":
        try:
            mise_taille = int(request.form.get("mise_taille") or 0)
            mise_total = int(request.form.get("mise_total") or 0)
            mise_numero = int(request.form.get("mise_numero") or 0)
            mise_triple = int(request.form.get("mise_triple") or 0)
            mise_totale = mise_taille + mise_total + mise_numero + mise_triple
            if (
                mise_totale >= 1
                and mise_totale <= solde
                and min(mise_taille, mise_total, mise_numero, mise_triple) >= 0
            ):
                solde -= mise_totale
                dee_tirer = sic_bo.lancer_des()
                gain_total = 0
                choix_taille = request.form.get("choix_taille")
                if mise_taille > 0 and choix_taille == sic_bo.trouver_taille(dee_tirer):
                    gain_total += mise_taille * 2
                choix_total = int(request.form.get("choix_total") or 0)
                if (
                    mise_total > 0
                    and sum(dee_tirer) == choix_total
                    and choix_total in sic_bo.GAIN_TOTAL
                ):
                    gain_total += mise_total * sic_bo.GAIN_TOTAL[choix_total]
                choix_numero = int(request.form.get("choix_numero") or 0)
                if mise_numero > 0:
                    gain_total += sic_bo.gain_numero(
                        dee_tirer, choix_numero, mise_numero
                    )
                if mise_triple > 0 and sic_bo.est_triple(dee_tirer):
                    gain_total += mise_triple * 31
                solde += gain_total
                sauvegarder_solde(solde)
                message = f"vous avez gagné un total de : {gain_total}"
            else:
                message = "choisissez une option valide"
        except ValueError:
            message = "choisissez une option valide"
        session["message"] = message
        session["dee_tirer"] = dee_tirer
        return redirect(url_for("page_sic_bo"))
    return render_template(
        "sic_bo.html", solde=solde, dee_tirer=dee_tirer, message=message
    )


@app.route("/roulette", methods=["GET", "POST"])
def page_roulette():
    message = session.pop("message", None)
    numero = session.pop("numero", None)
    solde = charger_solde()
    if request.method == "POST":
        try:
            mise_couleur = int(request.form.get("mise_couleur") or 0)
            mise_numero = int(request.form.get("mise_numero") or 0)
            mise_parite = int(request.form.get("mise_parite") or 0)
            mise_moitie = int(request.form.get("mise_moitie") or 0)
            mise_douzaine = int(request.form.get("mise_douzaine") or 0)
            mise_total = (
                mise_couleur + mise_numero + mise_parite + mise_moitie + mise_douzaine
            )
            if (
                mise_total >= 1
                and mise_total <= solde
                and min(
                    mise_couleur, mise_numero, mise_parite, mise_moitie, mise_douzaine
                )
                >= 0
            ):
                solde -= mise_total
                numero = roulette.lancer_bille()
                gain_total = 0
                choix_couleur = request.form.get("choix_couleur")
                if mise_couleur > 0 and choix_couleur == roulette.trouver_couleur(
                    numero
                ):
                    gain_total += mise_couleur * 2
                choix_numero = int(request.form.get("choix_numero") or 0)
                if mise_numero > 0 and choix_numero == numero:
                    gain_total += mise_numero * 36
                choix_parite = request.form.get("choix_parite")
                if mise_parite > 0 and choix_parite == roulette.trouver_parite(numero):
                    gain_total += mise_parite * 2
                choix_moitie = request.form.get("choix_moitie")
                if mise_moitie > 0 and choix_moitie == roulette.trouver_moitie(numero):
                    gain_total += mise_moitie * 2
                choix_douzaine = int(request.form.get("choix_douzaine") or 0)
                if mise_douzaine > 0 and choix_douzaine == roulette.trouver_douzaine(
                    numero
                ):
                    gain_total += mise_douzaine * 3
                solde += gain_total
                sauvegarder_solde(solde)
                message = f"vous avez gagné un total de : {gain_total}"
            else:
                message = "choisissez une option valide"
        except ValueError:
            message = "choisissez une option valide"
        session["message"] = message
        session["numero"] = numero
        return redirect(url_for("page_roulette"))
    return render_template("roulette.html", solde=solde, numero=numero, message=message)


@app.route("/bingo", methods=["GET", "POST"])
def page_bingo():
    message = session.pop("message", None)
    grille = session.pop("grille", None)
    nb_boules = session.pop("nb_boules", None)
    solde = charger_solde()
    if request.method == "POST":
        try:
            mise = int(request.form.get("mise"))
            if mise >= 1 and mise <= solde:
                solde -= mise
                grille = bingo.creer_grille()
                nb_boules = bingo.tirer_jusqu_au_bingo(grille)
                gain = mise * bingo.calculer_multiplicateur(nb_boules)
                solde += gain
                sauvegarder_solde(solde)
                message = (
                    f"nombre de boule nécessaire au bingo : {nb_boules}, gain : {gain}"
                )
            else:
                message = "choisissez une option valide"
        except ValueError:
            message = "choisissez une option valide"
        session["message"] = message
        session["grille"] = grille
        session["nb_boules"] = nb_boules
        return redirect(url_for("page_bingo"))
    return render_template(
        "bingo.html",
        solde=solde,
        grille=grille,
        nb_boules=nb_boules,
        message=message,
    )


@app.route("/craps", methods=["GET", "POST"])
def page_craps():
    message = session.pop("message", None)
    point = session.get("point")
    solde = charger_solde()
    if request.method == "POST":
        if "camp" in request.form:
            try:
                mise = int(request.form.get("mise"))
                camp = request.form.get("camp")
                if mise >= 1 and mise <= solde and camp in ["passer", "ne pas passer"]:
                    solde -= mise
                    total = craps.lancer_des()
                    resultat = craps.premier_lancer(total)
                    if resultat == "point":
                        session["point"] = total
                        session["mise"] = mise
                        session["camp"] = camp
                        sauvegarder_solde(solde)
                        message = f"point du joueur : {total}"
                    else:
                        resultat = craps.appliquer_camp(resultat, camp)
                        if resultat == "gagne":
                            gain = mise * 2
                            solde += gain
                            message = f"gain gagné : {gain}, dés tirer : {total}"
                        elif resultat == "egalite":
                            solde += mise
                            message = f"égalité mise rendue, dés tirer : {total}"
                        else:
                            message = f"perdu, dés tirer : {total}"
                        sauvegarder_solde(solde)
                else:
                    message = "choisissez une option valide"
            except ValueError:
                message = "choisissez une option valide"
        elif "cote" in request.form and "point" in session:
            try:
                mise = session.get("mise")
                camp = session.get("camp")
                cote = int(request.form.get("cote") or 0)
                cote_max = craps.calculer_cote_max(mise, point, solde, camp)
                if cote >= 0 and cote <= cote_max:
                    solde -= cote
                    resultat = craps.jouer_le_point(point)
                    resultat = craps.appliquer_camp(resultat, camp)
                    if resultat == "gagne":
                        gain = mise * 2
                        solde += gain
                        message = f"gain gagné : {gain}"
                        if cote > 0:
                            if camp == "passer":
                                paiement = craps.PAIEMENT_COTE[point]
                            else:
                                paiement = craps.PAIEMENT_COTE_NE_PAS_PASSER[point]
                            gain_cote = round(cote * paiement, 2)
                            solde += cote + gain_cote
                            message += f", gain de la cote : {gain_cote}"
                    else:
                        message = "perdu"
                    sauvegarder_solde(solde)
                    session.pop("point")
                    session.pop("mise")
                    session.pop("camp")
                else:
                    message = "choisissez une option valide"
            except ValueError:
                message = "choisissez une option valide"
        session["message"] = message
        return redirect(url_for("page_craps"))
    return render_template("craps.html", solde=solde, point=point, message=message)


@app.route("/mines", methods=["GET", "POST"])
def page_mines():
    message = session.pop("message", None)
    solde = charger_solde()
    partie_id = session.get("partie_mines")
    partie = parties.get(partie_id)
    if request.method == "POST":
        if "mise" in request.form:
            try:
                mise = int(request.form.get("mise"))
                if mise >= 1 and mise <= solde:
                    solde -= mise
                    sauvegarder_solde(solde)
                    grille = mine.creer_grille("?")
                    bombe = mine.creer_grille("V")
                    mine.placer_bombe(bombe)
                    partie_id = secrets.token_hex(16)
                    parties[partie_id] = {
                        "grille": grille,
                        "bombe": bombe,
                        "gain": mise,
                        "cases_trouvees": 0,
                    }
                    session["partie_mines"] = partie_id
                else:
                    message = "choisissez une option valide"
            except ValueError:
                message = "choisissez une option valide"
        elif "case" in request.form and partie is not None:
            try:
                case = request.form.get("case")
                morceaux = case.split("-")
                ligne = int(morceaux[0])
                colonne = int(morceaux[1])
                if ligne in range(mine.TAILLE) and colonne in range(mine.TAILLE):
                    if partie["grille"][ligne][colonne] == "✅":
                        message = "case déjà choisie"
                    elif partie["bombe"][ligne][colonne] == "B":
                        message = "perdu"
                        parties.pop(partie_id)
                        session.pop("partie_mines")
                    else:
                        partie["grille"][ligne][colonne] = "✅"
                        partie["gain"] = round(
                            partie["gain"]
                            * mine.calculer_multiplicateur(partie["cases_trouvees"]),
                            2,
                        )
                        partie["cases_trouvees"] += 1
                        if (
                            partie["cases_trouvees"]
                            == mine.TAILLE * mine.TAILLE - mine.NB_BOMBES
                        ):
                            solde += partie["gain"]
                            sauvegarder_solde(solde)
                            message = f"victoire vous avez gagné : {partie['gain']}"
                            parties.pop(partie_id)
                            session.pop("partie_mines")
                else:
                    message = "case invalide"
            except (ValueError, IndexError):
                message = "choisissez une option valide"
        elif request.form.get("action") == "encaisser" and partie is not None:
            solde += partie["gain"]
            sauvegarder_solde(solde)
            message = f"vous avez gagné : {partie['gain']}"
            parties.pop(partie_id)
            session.pop("partie_mines")
        session["message"] = message
        return redirect(url_for("page_mines"))
    return render_template("mines.html", solde=solde, partie=partie, message=message)


@app.route("/video-poker", methods=["GET", "POST"])
def page_video_poker():
    message = session.pop("message", None)
    main_finale = session.pop("main_finale", None)
    solde = charger_solde()
    partie_id = session.get("partie_video_poker")
    partie = parties.get(partie_id)
    if request.method == "POST":
        if "mise" in request.form:
            try:
                mise = int(request.form.get("mise"))
                if mise >= 1 and mise <= solde:
                    solde -= mise
                    sauvegarder_solde(solde)
                    paquet = créer_paquet()
                    main = video_poker.distribuer(paquet)
                    partie_id = secrets.token_hex(16)
                    parties[partie_id] = {"paquet": paquet, "main": main, "mise": mise}
                    session["partie_video_poker"] = partie_id
                else:
                    message = "choisissez une option valide"
            except ValueError:
                message = "choisissez une option valide"
        elif request.form.get("action") in ["echanger", "tout"] and partie is not None:
            if request.form.get("action") == "tout":
                choix = ["tout"]
            else:
                choix = request.form.getlist("garder")
            video_poker.echanger_carte(partie["main"], partie["paquet"], choix)
            combinaison = video_poker.evaluer_video_poker(partie["main"])
            gain = partie["mise"] * video_poker.GAIN[combinaison]
            solde += gain
            sauvegarder_solde(solde)
            message = f"combinaison : {combinaison}, vous avez gagné : {gain}"
            session["main_finale"] = partie["main"]
            parties.pop(partie_id)
            session.pop("partie_video_poker")
        session["message"] = message
        return redirect(url_for("page_video_poker"))
    return render_template(
        "video_poker.html",
        solde=solde,
        partie=partie,
        main_finale=main_finale,
        message=message,
    )


@app.route("/caribbean-stud", methods=["GET", "POST"])
def page_caribbean_stud():
    message = session.pop("message", None)
    main_croupier_final = session.pop("main_croupier_final", None)
    solde = charger_solde()
    partie_id = session.get("partie_caribbean_stud")
    partie = parties.get(partie_id)
    if request.method == "POST":
        if "mise" in request.form:
            try:
                mise = int(request.form.get("mise"))
                if mise >= 1 and mise <= solde // 3:
                    solde -= mise
                    sauvegarder_solde(solde)
                    paquet = caribbean_stud.créer_paquet()
                    main_joueur, main_croupier = caribbean_stud.distribuer(paquet)
                    partie_id = secrets.token_hex(16)
                    parties[partie_id] = {
                        "main_joueur": main_joueur,
                        "main_croupier": main_croupier,
                        "mise": mise,
                    }
                    session["partie_caribbean_stud"] = partie_id
                else:
                    message = "choisissez une option valide"
            except ValueError:
                message = "choisissez une option valide"
        elif request.form.get("action") == "coucher" and partie is not None:
            message = "mise perdu"
            parties.pop(partie_id)
            session.pop("partie_caribbean_stud")
        elif request.form.get("action") == "jouer" and partie is not None:
            relance = partie["mise"] * 2
            if relance <= solde:
                solde -= relance
                resultat, gain = caribbean_stud.calculer_gain(
                    partie["main_joueur"], partie["main_croupier"], partie["mise"]
                )
                solde += gain
                message = f"résultat : {resultat}, vous avez gagné : {gain}"
                session["main_croupier_final"] = partie["main_croupier"]
                parties.pop(partie_id)
                session.pop("partie_caribbean_stud")
                sauvegarder_solde(solde)
            else:
                message = "solde insuffisant pour relancer"
        session["message"] = message
        return redirect(url_for("page_caribbean_stud"))
    return render_template(
        "caribbean_stud.html",
        solde=solde,
        partie=partie,
        main_croupier_final=main_croupier_final,
        message=message,
    )


@app.route("/blackjack", methods=["GET", "POST"])
def page_blackjack():
    message = session.pop("message", None)
    main_croupier_final = session.pop("main_croupier_final", None)
    mains_final = session.pop("mains_final", None)
    solde = charger_solde()
    partie_id = session.get("partie_blackjack")
    partie = parties.get(partie_id)
    if request.method == "POST":
        if "mise" in request.form:
            try:
                mise = int(request.form.get("mise"))
                if mise >= 1 and mise <= solde:
                    solde -= mise
                    sauvegarder_solde(solde)
                    paquet = blackjack.créer_paquet()
                    main_joueur, main_croupier = blackjack.distribuer(paquet)
                    resultat = blackjack.verifier_blackjacks(main_joueur, main_croupier)
                    if resultat is not None:
                        gain = round(mise * blackjack.GAIN[resultat], 2)
                        solde += gain
                        sauvegarder_solde(solde)
                        message = f"{resultat} vous avez gagné : {gain}"
                        session["main_croupier_final"] = main_croupier
                        session["mains_final"] = [main_joueur]
                    else:
                        partie_id = secrets.token_hex(16)
                        parties[partie_id] = {
                            "paquet": paquet,
                            "main_croupier": main_croupier,
                            "mains": [main_joueur],
                            "mises": [mise],
                            "as_splittes": [False],
                            "en_cours": 0,
                        }
                        session["partie_blackjack"] = partie_id
                else:
                    message = "choisissez une option valide"
            except ValueError:
                message = "choisissez une option valide"
        elif request.form.get("action") == "stop" and partie is not None:
            partie["en_cours"] += 1
        elif request.form.get("action") == "hit" and partie is not None:
            main = partie["mains"][partie["en_cours"]]
            main.append(partie["paquet"].pop())
            if blackjack.points_main(main) > 21:
                partie["en_cours"] += 1
        elif request.form.get("action") == "doubler" and partie is not None:
            main = partie["mains"][partie["en_cours"]]
            i = partie["en_cours"]
            if len(main) == 2 and solde >= partie["mises"][i]:
                solde -= partie["mises"][i]
                sauvegarder_solde(solde)
                partie["mises"][i] = partie["mises"][i] * 2
                main.append(partie["paquet"].pop())
                partie["en_cours"] += 1
            else:
                message = "solde insuffisant pour doubler"
        elif request.form.get("action") == "split" and partie is not None:
            main = partie["mains"][partie["en_cours"]]
            i = partie["en_cours"]
            if (
                "split" in blackjack.options_possibles(main)
                and solde >= partie["mises"][i]
                and len(partie["mains"]) < 4
            ):
                solde -= partie["mises"][i]
                sauvegarder_solde(solde)
                carte = main.pop()
                partie["mains"].append([carte])
                partie["mises"].append(partie["mises"][i])
                main.append(partie["paquet"].pop())
                partie["mains"][-1].append(partie["paquet"].pop())
                if carte["valeur"] == "As":
                    partie["as_splittes"][i] = True
                    partie["as_splittes"].append(True)
                else:
                    partie["as_splittes"][i] = False
                    partie["as_splittes"].append(False)
            else:
                message = "split impossible"
        while (
            partie is not None
            and partie["en_cours"] < len(partie["mains"])
            and partie["as_splittes"][partie["en_cours"]] == True
        ):
            partie["en_cours"] += 1
        if partie is not None and partie["en_cours"] >= len(partie["mains"]):
            blackjack.jouer_croupier(partie["main_croupier"], partie["paquet"])
            gain_total = 0
            for i in range(len(partie["mains"])):
                resultat = blackjack.resultat_main(
                    partie["mains"][i], partie["main_croupier"]
                )
                gain = round(partie["mises"][i] * blackjack.GAIN[resultat], 2)
                solde += gain
                gain_total += gain
            sauvegarder_solde(solde)
            message = f"vous avez gagné un total de : {gain_total}"
            session["main_croupier_final"] = partie["main_croupier"]
            session["mains_final"] = partie["mains"]
            session.pop("partie_blackjack")
            parties.pop(partie_id)
        session["message"] = message
        return redirect(url_for("page_blackjack"))
    options = None
    if partie is not None:
        options = blackjack.options_possibles(partie["mains"][partie["en_cours"]])
    return render_template(
        "blackjack.html",
        solde=solde,
        partie=partie,
        main_croupier_final=main_croupier_final,
        mains_final=mains_final,
        options=options,
        message=message,
    )


if __name__ == "__main__":
    app.run(debug=True)
