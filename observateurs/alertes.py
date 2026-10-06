from observateurs.observateur import Observateur
import tkinter as tk

class Alertes(Observateur):

    def __init__(self, fenetre):
        self._frame_alertes = tk.LabelFrame(fenetre, text="Alertes", padx=10, pady=10)
        self._frame_alertes.pack(fill=tk.X, padx=10, pady=5)
        self._label_alertes = tk.Label(
            self._frame_alertes, text="Aucune alerte", fg="gray", justify=tk.LEFT, wraplength=380
        )
        self._label_alertes.pack(anchor="w")

    def actualiser(self,sujet):
        donnees = sujet.get_donnees()
        titres = donnees["titres"]

        alertes = []

        for ticker, titre in titres.items():

            # Les données du titre
            prix = titre["prix"]
            seuil_haut = titre["seuil_haut"]
            seuil_bas = titre["seuil_bas"]
            if prix <= 0:
                continue

            if prix >= seuil_haut:
                alertes.append(
                    f"⚠️ {ticker} dépasse le seuil haut "
                    f"({prix:.2f} $ ≥ {seuil_haut:.2f} $)"
                )

            elif prix <= seuil_bas:
                alertes.append(
                    f"⚠️ {ticker} sous le seuil bas "
                    f"({prix:.2f} $ ≤ {seuil_bas:.2f} $)"
                )

        self._label_alertes.config(
            text="\n".join(alertes) if alertes else "Aucune alerte",
            fg="red" if alertes else "gray",
        )
