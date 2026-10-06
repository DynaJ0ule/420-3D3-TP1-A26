import tkinter as tk
from datetime import datetime
import yfinance as yf

from modeles.portfolio import Portfolio
from modeles.titre import Titre

from observateurs.prix_temps_reel import PrixTempsReel
from observateurs.liste_gestion import ListeGestion
from observateurs.total import Total
from observateurs.alertes import Alertes
from observateurs.mise_a_jour import MiseAJour
from observateurs.logger import Logger
from modeles.utils import Utils

TITRES = {
    "AAPL":  {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0},
    "GOOGL": {"quantite": 5,  "seuil_haut": 160.0, "seuil_bas": 120.0},
    "MSFT":  {"quantite": 8,  "seuil_haut": 430.0, "seuil_bas": 380.0},
}

INTERVALLE_MS = 30000  # Fréquence de rafraîchissement des prix (30 secondes)

# Polices utilisées dans toute l'interface, centralisées ici pour rester cohérentes
POLICE = ("Segoe UI", 10)
POLICE_TITRE = ("Segoe UI", 16, "bold")
POLICE_VALEUR = ("Segoe UI", 13, "bold")



class DashboardTitres:
    def __init__(self):

        portfolio = Portfolio()
        for ticker, donnees in TITRES.items():
            Portfolio.ajouter_titre(ticker, donnees)
        self.fenetre = tk.Tk()
        self.fenetre.title("Portfolio Tracker")
        self.fenetre.resizable(False, False)
        self.fenetre.option_add("*Font", POLICE)

        tk.Label(self.fenetre, text="Portfolio Tracker", font=POLICE_TITRE).pack(pady=10)

        gestion_frame = tk.LabelFrame(self.fenetre, text="Gérer les titres", padx=10, pady=10)
        gestion_frame.pack(fill=tk.X, padx=10, pady=5)

        self.prix_temps_reel = PrixTempsReel(self.fenetre)

        

        # Ligne 1 : formulaire d'ajout d'un nouveau titre
        ligne_ajout = tk.Frame(gestion_frame)
        ligne_ajout.pack(fill=tk.X)
        self.entry_ticker = self._champ(ligne_ajout, "Ticker", width=8)
        self.entry_quantite = self._champ(ligne_ajout, "Qté", width=5, valeur_defaut="1")
        self.entry_seuil_bas_ajout = self._champ(ligne_ajout, "Alerte basse", width=7)
        self.entry_seuil_haut_ajout = self._champ(ligne_ajout, "Alerte haute", width=7)
        tk.Button(ligne_ajout, text="Ajouter", command=self.ajouter_titre).pack(side=tk.LEFT)

        tk.Label(
            gestion_frame,
            text="(Alertes optionnelles : si vides, calculées à ±20% du prix actuel)",
            font=("Segoe UI", 8), fg="gray"
        ).pack(anchor="w", pady=(2, 5))

        # Ligne 2 : liste des titres actuellement dans le portefeuille + retrait
        # (la sélection dans cette liste sert aussi au formulaire de modification ci-dessous)
        self.liste_gestion = ListeGestion(self.gestion_frame)
        tk.Button(gestion_frame, text="Retirer", command=self.retirer_titre).pack(side=tk.LEFT, padx=(5, 0), anchor="n")

        # Ligne 3 : modification de la quantité et/ou des seuils du titre sélectionné
        ligne_modif = tk.Frame(gestion_frame)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))
        tk.Label(ligne_modif, text="Sélection →").pack(side=tk.LEFT)
        self.entry_nouvelle_quantite = self._champ(ligne_modif, "Qté", width=5)
        self.entry_nouveau_seuil_bas = self._champ(ligne_modif, "Alerte basse", width=7)
        self.entry_nouveau_seuil_haut = self._champ(ligne_modif, "Alerte haute", width=7)
        tk.Button(ligne_modif, text="Modifier sélection", command=self.modifier_selection).pack(side=tk.LEFT)

        # Message de statut (succès / erreur) pour les actions de cette section
        self.label_statut_titres = tk.Label(gestion_frame, text="", font=("Segoe UI", 9), fg="gray")
        self.label_statut_titres.pack(anchor="w", pady=(5, 0))

        # Section "Mon portfolio" : valeur totale et variation depuis l'ouverture
        self.portfolio = Total(self.fenetre)

        # Section "Alertes" : liste des titres ayant franchi un seuil, ou message par défaut
        self.alertes = Alertes(self.fenetre)

        # Premier chargement des prix, puis boucle de rafraîchissement automatique
        # (rafraichir() se replanifie elle-même via fenetre.after)
        self.rafraichir()
        self.fenetre.mainloop()

    def _champ(self, parent, texte, width, valeur_defaut=""):
        """Ajoute un couple Label + Entry à `parent` et retourne l'Entry."""
        tk.Label(parent, text=f"{texte}:").pack(side=tk.LEFT)
        entry = tk.Entry(parent, width=width)
        if valeur_defaut:
            entry.insert(0, valeur_defaut)
        entry.pack(side=tk.LEFT, padx=(2, 8))
        return entry

    
