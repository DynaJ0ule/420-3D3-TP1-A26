import tkinter as tk
from tkinter import messagebox

import yfinance as yf

from modeles.portfolio import Portfolio
from modeles.titre import Titre

from observateurs.prix_temps_reel import PrixTempsReel
from observateurs.liste_gestion import ListeGestion
from observateurs.total import Total
from observateurs.alertes import Alertes
from observateurs.mise_a_jour import MiseAJour
from observateurs.logger import Logger
from observateurs.tableau_de_bord import TableauDeBord


INTERVALLE_MS = 30000


def recuperer_prix(ticker):
    action = yf.Ticker(ticker)

    fast_info = action.fast_info

    prix = fast_info.get("last_price")
    ouverture = fast_info.get("open")

    if prix is None:
        raise ValueError(
            f"Impossible de récupérer le prix de {ticker}"
        )

    if ouverture is None:
        ouverture = prix

    return prix, ouverture


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Portfolio Tracker")
        self.root.geometry("850x650")

        self.portfolio = Portfolio()

        self.prix_observateurs = {}

        self.creer_portfolio_initial()

        self.creer_observateurs()

        self.creer_interface()

        self.rafraichir()

    # --------------------------------------------------
    # PORTFOLIO
    # --------------------------------------------------

    def creer_portfolio_initial(self):
        titres = [
            Titre("AAPL", 10, 200, 150),
            Titre("GOOGL", 5, 160, 120),
            Titre("MSFT", 8, 430, 380)
        ]

        for titre in titres:
            self.portfolio.ajouter_titre(titre)

    # --------------------------------------------------
    # OBSERVATEURS
    # --------------------------------------------------

    def creer_observateurs(self):

        self.liste_observateur = ListeGestion(
            self.portfolio,
            self.actualiser_liste
        )

        self.total_observateur = Total(
            self.portfolio,
            self.actualiser_total
        )

        self.alertes_observateur = Alertes(
            self.portfolio,
            self.actualiser_alertes
        )

        self.mise_a_jour_observateur = MiseAJour(
            self.actualiser_date
        )

        self.logger_observateur = Logger(
            self.portfolio
        )

        self.tableau_observateur = TableauDeBord(
            self.portfolio,
            self.actualiser_tableau
        )

        self.portfolio.abonner(
            self.liste_observateur
        )

        self.portfolio.abonner(
            self.total_observateur
        )

        self.portfolio.abonner(
            self.alertes_observateur
        )

        self.portfolio.abonner(
            self.logger_observateur
        )

        self.portfolio.abonner(
            self.tableau_observateur
        )

    # --------------------------------------------------
    # INTERFACE
    # --------------------------------------------------

    def creer_interface(self):

        titre = tk.Label(
            self.root,
            text="PORTFOLIO TRACKER",
            font=("Arial", 20, "bold")
        )

        titre.pack(pady=10)

        # Liste
        cadre_liste = tk.LabelFrame(
            self.root,
            text="Titres"
        )

        cadre_liste.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.liste = tk.Listbox(
            cadre_liste,
            height=10
        )

        self.liste.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Total
        self.label_total = tk.Label(
            self.root,
            text="Valeur totale : 0.00 $",
            font=("Arial", 14)
        )

        self.label_total.pack(pady=5)

        self.label_variation = tk.Label(
            self.root,
            text="Variation : 0.00 %",
            font=("Arial", 12)
        )

        self.label_variation.pack(pady=5)

        # Tableau
        self.label_tableau = tk.Label(
            self.root,
            text="Nombre de titres : 0 | Quantité : 0"
        )

        self.label_tableau.pack(pady=5)

        # Alertes
        cadre_alertes = tk.LabelFrame(
            self.root,
            text="Alertes"
        )

        cadre_alertes.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.label_alertes = tk.Label(
            cadre_alertes,
            text="Aucune alerte"
        )

        self.label_alertes.pack(
            padx=10,
            pady=10
        )

        # Date
        self.label_date = tk.Label(
            self.root,
            text="Dernière mise à jour : --"
        )

        self.label_date.pack(pady=5)

        # Ajout
        cadre_ajout = tk.LabelFrame(
            self.root,
            text="Ajouter un titre"
        )

        cadre_ajout.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            cadre_ajout,
            text="Ticker"
        ).grid(row=0, column=0)

        self.entry_ticker = tk.Entry(
            cadre_ajout
        )

        self.entry_ticker.grid(
            row=0,
            column=1
        )

        tk.Label(
            cadre_ajout,
            text="Quantité"
        ).grid(row=0, column=2)

        self.entry_quantite = tk.Entry(
            cadre_ajout
        )

        self.entry_quantite.grid(
            row=0,
            column=3
        )

        tk.Label(
            cadre_ajout,
            text="Seuil haut"
        ).grid(row=1, column=0)

        self.entry_haut = tk.Entry(
            cadre_ajout
        )

        self.entry_haut.grid(
            row=1,
            column=1
        )

        tk.Label(
            cadre_ajout,
            text="Seuil bas"
        ).grid(row=1, column=2)

        self.entry_bas = tk.Entry(
            cadre_ajout
        )

        self.entry_bas.grid(
            row=1,
            column=3
        )

        tk.Button(
            cadre_ajout,
            text="Ajouter",
            command=self.ajouter_titre
        ).grid(
            row=2,
            column=0,
            columnspan=4,
            pady=5
        )

        # Bouton supprimer
        tk.Button(
            self.root,
            text="Supprimer la sélection",
            command=self.retirer_titre
        ).pack(pady=5)

    # --------------------------------------------------
    # AJOUTER
    # --------------------------------------------------

    def ajouter_titre(self):

        try:
            ticker = self.entry_ticker.get().upper()

            quantite = int(
                self.entry_quantite.get()
            )

            seuil_haut = float(
                self.entry_haut.get()
            )

            seuil_bas = float(
                self.entry_bas.get()
            )

            if not ticker:
                raise ValueError(
                    "Le ticker est obligatoire."
                )

            if quantite <= 0:
                raise ValueError(
                    "La quantité doit être positive."
                )

            prix, ouverture = recuperer_prix(
                ticker
            )

            titre = Titre(
                ticker,
                quantite,
                seuil_haut,
                seuil_bas
            )

            # Observateur du titre
            observateur_prix = PrixTempsReel(
                titre,
                self.actualiser_prix
            )

            titre.abonner(
                observateur_prix
            )

            self.prix_observateurs[ticker] = (
                observateur_prix
            )

            titre.mettre_a_jour_prix(
                prix,
                ouverture
            )

            self.portfolio.ajouter_titre(
                titre
            )

            self.mise_a_jour_observateur.actualiser()

            messagebox.showinfo(
                "Succès",
                f"{ticker} a été ajouté."
            )

            self.vider_champs()

        except ValueError as erreur:

            messagebox.showerror(
                "Erreur",
                str(erreur)
            )

        except Exception as erreur:

            messagebox.showerror(
                "Erreur",
                f"Erreur : {erreur}"
            )

    # --------------------------------------------------
    # SUPPRIMER
    # --------------------------------------------------

    def retirer_titre(self):

        selection = self.liste.curselection()

        if not selection:
            messagebox.showwarning(
                "Attention",
                "Sélectionnez un titre."
            )
            return

        ligne = self.liste.get(
            selection[0]
        )

        ticker = ligne.split(" - ")[0]

        self.portfolio.retirer_titre(
            ticker
        )

        if ticker in self.prix_observateurs:
            del self.prix_observateurs[ticker]

        self.mise_a_jour_observateur.actualiser()

    # --------------------------------------------------
    # OBSERVATEUR PRIX
    # --------------------------------------------------

    def actualiser_prix(
        self,
        ticker,
        prix,
        variation
    ):

        # La liste est mise à jour par ListeGestion.
        pass

    # --------------------------------------------------
    # OBSERVATEUR LISTE
    # --------------------------------------------------

    def actualiser_liste(self, titres):

        self.liste.delete(
            0,
            tk.END
        )

        for ticker, titre in titres.items():

            prix = titre["prix"]

            variation = 0

            if titre["ouverture"] != 0:
                variation = (
                    (prix - titre["ouverture"])
                    / titre["ouverture"]
                ) * 100

            self.liste.insert(
                tk.END,
                f"{ticker} - "
                f"{prix:.2f} $ "
                f"({variation:+.2f} %)"
            )

    # --------------------------------------------------
    # OBSERVATEUR TOTAL
    # --------------------------------------------------

    def actualiser_total(
        self,
        total,
        variation
    ):

        self.label_total.config(
            text=f"Valeur totale : {total:.2f} $"
        )

        self.label_variation.config(
            text=f"Variation : {variation:+.2f} %"
        )

    # --------------------------------------------------
    # OBSERVATEUR ALERTES
    # --------------------------------------------------

    def actualiser_alertes(self, alertes):

        if not alertes:

            self.label_alertes.config(
                text="Aucune alerte"
            )

        else:

            self.label_alertes.config(
                text="\n".join(alertes)
            )

    # --------------------------------------------------
    # OBSERVATEUR MISE À JOUR
    # --------------------------------------------------

    def actualiser_date(self, date):

        self.label_date.config(
            text=f"Dernière mise à jour : {date}"
        )

    # --------------------------------------------------
    # OBSERVATEUR TABLEAU
    # --------------------------------------------------

    def actualiser_tableau(
        self,
        nombre,
        quantite
    ):

        self.label_tableau.config(
            text=(
                f"Nombre de titres : {nombre} | "
                f"Quantité : {quantite}"
            )
        )

    # --------------------------------------------------
    # RAFRAÎCHISSEMENT
    # --------------------------------------------------

    def rafraichir(self):

        try:

            prix_actuels = {}

            for ticker in self.portfolio.get_titres():

                prix, ouverture = recuperer_prix(
                    ticker
                )

                prix_actuels[ticker] = {
                    "prix": prix,
                    "ouverture": ouverture
                }

            self.portfolio.mise_a_jour(
                prix_actuels
            )

            self.mise_a_jour_observateur.actualiser()

        except Exception as erreur:

            print(
                f"Erreur lors du rafraîchissement : {erreur}"
            )

        self.root.after(
            INTERVALLE_MS,
            self.rafraichir
        )

    # --------------------------------------------------
    # UTILITAIRE
    # --------------------------------------------------

    def vider_champs(self):

        self.entry_ticker.delete(
            0,
            tk.END
        )

        self.entry_quantite.delete(
            0,
            tk.END
        )

        self.entry_haut.delete(
            0,
            tk.END
        )

        self.entry_bas.delete(
            0,
            tk.END
        )

    # --------------------------------------------------
    # LANCER
    # --------------------------------------------------

    def lancer(self):
        self.root.mainloop()