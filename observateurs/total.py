from observateurs.observateur import Observateur
import tkinter as tk

class Total(Observateur):
    def __init__(self, fenetre):
        frame_portfolio = tk.LabelFrame(fenetre, text="Mon portfolio", padx=10, pady=10)
        frame_portfolio.pack(fill=tk.X, padx=10, pady=5)
        self.label_valeur = tk.Label(frame_portfolio, text="Valeur totale : calcul en cours...", font=POLICE_VALEUR)
        self.label_valeur.pack()
        self.label_variation = tk.Label(frame_portfolio, text="")
        self.label_variation.pack()

    def actualiser(self, portfolio):
        titres = portfolio.get_donnees()

        total = sum(
            titre["prix"] * titre["quantite"]
            for titre in titres.values()
        )

        valeur_ouverture = sum(
            titre["ouverture"] * titre["quantite"]
            for titre in titres.values()
        )

        variation = (
            (total - valeur_ouverture) / valeur_ouverture * 100
            if valeur_ouverture
            else 0
        )

        self._callback(total, variation)