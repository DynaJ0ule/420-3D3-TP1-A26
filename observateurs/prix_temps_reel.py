from observateurs.observateur import Observateur
import tkinter as tk



class PrixTempsReel(Observateur):
    def __init__(self, fenetre):
        self._fenetre = fenetre
        self._labels_titre = {}
        self._frames_titre = {}
        self._frame_titres = tk.LabelFrame(self._fenetre, text="Prix en temps réel", padx=10, pady=10)
        self._frame_titres.pack(fill=tk.X, padx=10, pady=5)

    def _creer_ligne_prix(self, ticker):
        """Ajoute la ligne d'affichage de prix pour un ticker (appelé au
        démarrage pour chaque titre, et à nouveau quand un titre est ajouté)."""
        frame = tk.Frame(self._frame_titres)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=f"{ticker}:", width=8, font=("Segoe UI", 10, "bold"), anchor="w").pack(side=tk.LEFT)
        label = tk.Label(frame, text="Chargement...")
        label.pack(side=tk.LEFT)
        self._labels_prix[ticker] = label
        self._frames_prix[ticker] = frame

    def actualiser(self, sujet):
        for titre in sujet.get_donnees(): #TODO vérifier fonction
            texte, couleur = self.formater_prix (titre["prix"],titre["ouverture"])
            self._creer_ligne_prix(titre["ticker"])
            self._labels_prix[titre["ticker"]].config(text=texte, fg=couleur)
           
    def formater_prix(prix, ouverture):
        """Retourne le texte et la couleur à afficher pour un prix et sa variation
        par rapport à l'ouverture (vert si en hausse, rouge si en baisse)."""
        variation = (prix - ouverture) / ouverture * 100
        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"
        return f"{prix:.2f} $  {symbole} {abs(variation):.2f}%", couleur