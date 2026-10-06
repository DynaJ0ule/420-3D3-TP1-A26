from observateurs.observateur import Observateur
import tkinter as tk


class TableauDeBord(Observateur):

    def __init__(self, fenetre):
        self._label = tk.Label(
            fenetre,
            text="0 titres — 0 actions"
        )
        self._label.pack(pady=5)

    def actualiser(self, sujet):
        titres = sujet.get_donnees()["titres"]

        nombre_titres = len(titres)

        quantite_totale = sum(
            titre["quantite"]
            for titre in titres.values()
        )

        self._label.config(
            text=f"{nombre_titres} titres — {quantite_totale} actions"
        )