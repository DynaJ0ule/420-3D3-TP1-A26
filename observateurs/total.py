from observateurs.observateur import Observateur
import tkinter as tk


class Total(Observateur):

    def __init__(self, fenetre):
        frame_portfolio = tk.LabelFrame(
            fenetre,
            text="Mon portfolio",
            padx=10,
            pady=10
        )
        frame_portfolio.pack(
            fill=tk.X,
            padx=10,
            pady=5
        )

        self.label_valeur = tk.Label(
            frame_portfolio,
            text="Valeur totale : calcul en cours..."
        )
        self.label_valeur.pack()

        self.label_variation = tk.Label(
            frame_portfolio,
            text=""
        )
        self.label_variation.pack()


    def actualiser(self, sujet):
        titres = sujet.get_donnees()["titres"]

        total = sum(
            titre["prix"] * titre["quantite"]
            for titre in titres.values()
        )

        valeur_ouverture = sum(
            titre["ouverture"] * titre["quantite"]
            for titre in titres.values()
        )

        if valeur_ouverture:
            variation = (
                (total - valeur_ouverture)
                / valeur_ouverture
                * 100
            )
        else:
            variation = 0

        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        self.label_valeur.config(
            text=f"Valeur totale : {total:.2f} $"
        )

        self.label_variation.config(
            text=f"{symbole} {abs(variation):.2f}% depuis l'ouverture",
            fg=couleur
        )
        