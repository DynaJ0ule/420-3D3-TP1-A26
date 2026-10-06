from observateurs.observateur import Observateur
import tkinter as tk


class PrixTempsReel(Observateur):

    def __init__(self, fenetre):
        self._fenetre = fenetre
        self._labels_prix = {}
        self._frames_prix = {}

        self._frame_titres = tk.LabelFrame(
            fenetre,
            text="Prix en temps réel",
            padx=10,
            pady=10
        )
        self._frame_titres.pack(fill=tk.X, padx=10, pady=5)

    def _creer_ligne_prix(self, ticker):
        frame = tk.Frame(self._frame_titres)
        frame.pack(fill=tk.X, pady=2)

        tk.Label(
            frame,
            text=f"{ticker}:",
            width=8,
            anchor="w"
        ).pack(side=tk.LEFT)

        label = tk.Label(frame, text="Chargement...")
        label.pack(side=tk.LEFT)

        self._labels_prix[ticker] = label
        self._frames_prix[ticker] = frame

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        titres = donnees["titres"]

        for ticker, titre in titres.items():

            if ticker not in self._labels_prix:
                self._creer_ligne_prix(ticker)

            texte, couleur = self.formater_prix(
                titre["prix"],
                titre["ouverture"]
            )

            self._labels_prix[ticker].config(
                text=texte,
                fg=couleur
            )

    def formater_prix(self, prix, ouverture):
        if ouverture == 0:
            return f"{prix:.2f} $", "black"

        variation = (prix - ouverture) / ouverture * 100
        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        return f"{prix:.2f} $  {symbole} {abs(variation):.2f}%", couleur
