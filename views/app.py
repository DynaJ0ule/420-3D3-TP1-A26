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

INTERVALLE_MS = 30000

POLICE = ("Segoe UI", 10)
POLICE_TITRE = ("Segoe UI", 16, "bold")
POLICE_VALEUR = ("Segoe UI", 13, "bold")

def recuperer_prix(ticker):
    """Retourne (prix, ouverture) avec yfinance."""
    try:
        info = yf.Ticker(ticker).fast_info
        prix = info["last_price"]
        ouverture = info["open"]

        if prix is None:
            raise ValueError(f"Le titre '{ticker}' n'existe pas.")

        return float(prix), float(ouverture)

    except Exception as e:
        print(f"Erreur yfinance pour {ticker} : {e}")
        raise Exception(f"Impossible de récupérer le prix de {ticker}") from e


def entier_positif(texte):
    valeur = int(texte)
    if valeur <= 0:
        raise ValueError
    return valeur


def flottant_positif(texte):
    valeur = float(texte)
    if valeur <= 0:
        raise ValueError
    return valeur


class App:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Portfolio Tracker")
        self.fenetre.resizable(False, False)
        self.fenetre.option_add("*Font", POLICE)

        self.portfolio = Portfolio()

        self.labels_prix = {}
        self.frames_prix = {}
        self.prix_observateurs = {}

        self.label_valeur = None
        self.label_variation = None
        self.label_alertes = None
        self.label_maj = None
        self.label_statut_titres = None

        self.creer_portfolio_initial()
        self.creer_observateurs()
        self.creer_interface()

    def creer_portfolio_initial(self):
        titres_initiaux = {
            "AAPL": (10, 200.0, 150.0),
            "GOOGL": (5, 160.0, 120.0),
            "MSFT": (8, 430.0, 380.0),
        }

        for ticker, (quantite, seuil_haut, seuil_bas) in titres_initiaux.items():
            titre = Titre(
                ticker,
                quantite,
                seuil_haut,
                seuil_bas,
            )

            self.portfolio.ajouter_titre(titre)

    def creer_observateurs(self):
        self.portfolio.abonner(
            ListeGestion(self.portfolio, self.actualiser_liste)
        )
        self.portfolio.abonner(
            Total(self.portfolio, self.actualiser_total)
        )
        self.portfolio.abonner(
            Alertes(self.portfolio, self.actualiser_alertes)
        )
        self.portfolio.abonner(
            Logger(self.portfolio)
        )
        self.portfolio.abonner(
            TableauDeBord(self.portfolio, self.actualiser_tableau_de_bord)
        )

        self.mise_a_jour_observateur = MiseAJour(
            self.actualiser_date
        )
        self.portfolio.abonner(self.mise_a_jour_observateur)

    def creer_interface(self):
        tk.Label(
            self.fenetre,
            text="Portfolio Tracker",
            font=POLICE_TITRE,
        ).pack(pady=10)

        self.frame_prix = tk.LabelFrame(
            self.fenetre,
            text="Prix en temps réel",
            padx=10,
            pady=10,
        )
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)

        self.creer_gestion()

        frame_portfolio = tk.LabelFrame(
            self.fenetre,
            text="Mon portfolio",
            padx=10,
            pady=10,
        )
        frame_portfolio.pack(fill=tk.X, padx=10, pady=5)

        self.label_valeur = tk.Label(
            frame_portfolio,
            text="Valeur totale : calcul en cours...",
            font=POLICE_VALEUR,
        )
        self.label_valeur.pack()

        self.label_variation = tk.Label(
            frame_portfolio,
            text="",
        )
        self.label_variation.pack()

        frame_alertes = tk.LabelFrame(
            self.fenetre,
            text="Alertes",
            padx=10,
            pady=10,
        )
        frame_alertes.pack(fill=tk.X, padx=10, pady=5)

        self.label_alertes = tk.Label(
            frame_alertes,
            text="Aucune alerte",
            fg="gray",
            justify=tk.LEFT,
            wraplength=500,
        )
        self.label_alertes.pack(anchor="w")

        self.label_maj = tk.Label(
            self.fenetre,
            text="",
            font=("Segoe UI", 9),
            fg="gray",
        )
        self.label_maj.pack(pady=5)

        for ticker in self.portfolio.get_titres():
            self._creer_ligne_prix(ticker)

    def creer_gestion(self):
        frame = tk.LabelFrame(
            self.fenetre,
            text="Gérer les titres",
            padx=10,
            pady=10,
        )
        frame.pack(fill=tk.X, padx=10, pady=5)

        ligne_ajout = tk.Frame(frame)
        ligne_ajout.pack(fill=tk.X)

        self.entry_ticker = self._champ(
            ligne_ajout, "Ticker", 8
        )
        self.entry_quantite = self._champ(
            ligne_ajout, "Qté", 5, "1"
        )
        self.entry_seuil_bas_ajout = self._champ(
            ligne_ajout, "Alerte basse", 7
        )
        self.entry_seuil_haut_ajout = self._champ(
            ligne_ajout, "Alerte haute", 7
        )

        tk.Button(
            ligne_ajout,
            text="Ajouter",
            command=self.ajouter_titre,
        ).pack(side=tk.LEFT)

        tk.Label(
            frame,
            text="(Alertes optionnelles : si vides, ±20% du prix actuel)",
            font=("Segoe UI", 8),
            fg="gray",
        ).pack(anchor="w", pady=(2, 5))

        ligne_liste = tk.Frame(frame)
        ligne_liste.pack(fill=tk.X)

        self.listbox_titres = tk.Listbox(
            ligne_liste,
            height=4,
            exportselection=False,
        )
        self.listbox_titres.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
        )

        tk.Button(
            ligne_liste,
            text="Retirer",
            command=self.retirer_titre,
        ).pack(side=tk.LEFT, padx=(5, 0), anchor="n")

        ligne_modif = tk.Frame(frame)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))

        tk.Label(
            ligne_modif,
            text="Sélection →",
        ).pack(side=tk.LEFT)

        self.entry_nouvelle_quantite = self._champ(
            ligne_modif, "Qté", 5
        )
        self.entry_nouveau_seuil_bas = self._champ(
            ligne_modif, "Alerte basse", 7
        )
        self.entry_nouveau_seuil_haut = self._champ(
            ligne_modif, "Alerte haute", 7
        )

        tk.Button(
            ligne_modif,
            text="Modifier sélection",
            command=self.modifier_selection,
        ).pack(side=tk.LEFT)

        self.label_statut_titres = tk.Label(
            frame,
            text="",
            font=("Segoe UI", 9),
            fg="gray",
        )
        self.label_statut_titres.pack(
            anchor="w",
            pady=(5, 0),
        )

        self.actualiser_liste(
            self.portfolio.get_donnees()["titres"]
        )

    def _champ(self, parent, texte, width, valeur_defaut=""):
        tk.Label(
            parent,
            text=f"{texte}:",
        ).pack(side=tk.LEFT)

        entry = tk.Entry(parent, width=width)

        if valeur_defaut:
            entry.insert(0, valeur_defaut)

        entry.pack(side=tk.LEFT, padx=(2, 8))
        return entry

    def _creer_ligne_prix(self, ticker):
        if ticker in self.frames_prix:
            return

        frame = tk.Frame(self.frame_prix)
        frame.pack(fill=tk.X, pady=2)

        tk.Label(
            frame,
            text=f"{ticker}:",
            width=8,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        ).pack(side=tk.LEFT)

        label = tk.Label(
            frame,
            text="Chargement...",
        )
        label.pack(side=tk.LEFT)

        self.labels_prix[ticker] = label
        self.frames_prix[ticker] = frame

        titre = self.portfolio.get_titre(ticker)
        observateur = PrixTempsReel(
            titre,
            self.actualiser_prix,
        )
        titre.abonner(observateur)
        self.prix_observateurs[ticker] = observateur

    def _texte_listbox(self, ticker):
        infos = self.portfolio.get_titre(ticker).get_donnees()

        return (
            f"{ticker} — {infos['quantite']} action(s) "
            f"(alerte : {infos['seuil_bas']:.2f} $ / "
            f"{infos['seuil_haut']:.2f} $)"
        )

    def _ticker_selectionne(self):
        selection = self.listbox_titres.curselection()

        if not selection:
            return None

        texte = self.listbox_titres.get(selection[0])
        return selection[0], texte.split(" — ")[0]

    def _statut(self, texte, couleur):
        self.label_statut_titres.config(
            text=texte,
            fg=couleur,
        )

    def actualiser_prix(self, ticker, prix, variation):
        if ticker not in self.labels_prix:
            return

        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        self.labels_prix[ticker].config(
            text=f"{prix:.2f} $  {symbole} {abs(variation):.2f}%",
            fg=couleur,
        )

    def actualiser_liste(self, titres):
        self.listbox_titres.delete(0, tk.END)

        for ticker in titres:
            self.listbox_titres.insert(
                tk.END,
                self._texte_listbox(ticker),
            )

    def actualiser_total(self, total, variation):
        self.label_valeur.config(
            text=f"Valeur totale : {total:.2f} $"
        )

        symbole = "▲" if variation >= 0 else "▼"

        self.label_variation.config(
            text=f"{symbole} {abs(variation):.2f}% depuis l'ouverture",
            fg="green" if variation >= 0 else "red",
        )

    def actualiser_alertes(self, alertes):
        self.label_alertes.config(
            text="\n".join(alertes) if alertes else "Aucune alerte",
            fg="red" if alertes else "gray",
        )

    def actualiser_date(self, date):
        self.label_maj.config(
            text=f"Dernière mise à jour : {date}",
            fg="gray",
        )

    def actualiser_tableau_de_bord(
        self,
        nombre_titres,
        quantite_totale,
    ):
        pass #bro.....

    def ajouter_titre(self):
        ticker = self.entry_ticker.get().strip().upper()

        if not ticker:
            return

        if ticker in self.portfolio.get_titres():
            self._statut(
                f"{ticker} est déjà dans le portfolio.",
                "orange",
            )
            return

        try:
            quantite = entier_positif(
                self.entry_quantite.get().strip()
            )
        except ValueError:
            self._statut(
                "La quantité doit être un nombre entier positif.",
                "red",
            )
            return

        texte_bas = self.entry_seuil_bas_ajout.get().strip()
        texte_haut = self.entry_seuil_haut_ajout.get().strip()

        try:
            seuil_bas = (
                flottant_positif(texte_bas)
                if texte_bas else None
            )
            seuil_haut = (
                flottant_positif(texte_haut)
                if texte_haut else None
            )
        except ValueError:
            self._statut(
                "Les alertes doivent être des nombres positifs.",
                "red",
            )
            return

        if (
            seuil_bas is not None
            and seuil_haut is not None
            and seuil_bas >= seuil_haut
        ):
            self._statut(
                "L'alerte basse doit être inférieure à l'alerte haute.",
                "red",
            )
            return

        try:
            prix, ouverture = recuperer_prix(ticker)
        except Exception:
            self._statut(
                f"Le titre '{ticker}' n'existe pas ou est inaccessible.",
                "red",
            )
            return

        seuil_haut = round(
            seuil_haut if seuil_haut is not None else prix * 1.2,
            2,
        )
        seuil_bas = round(
            seuil_bas if seuil_bas is not None else prix * 0.8,
            2,
        )

        titre = Titre(
            ticker,
            quantite,
            seuil_haut,
            seuil_bas,
        )

        self.portfolio.ajouter_titre(titre)
        titre.mettre_a_jour_prix(prix, ouverture)

        self._creer_ligne_prix(ticker)
        self.actualiser_prix(
            ticker,
            prix,
            ((prix - ouverture) / ouverture * 100)
            if ouverture else 0,
        )

        self.actualiser_liste(
            self.portfolio.get_donnees()["titres"]
        )

        for entry, valeur in (
            (self.entry_ticker, ""),
            (self.entry_quantite, "1"),
            (self.entry_seuil_bas_ajout, ""),
            (self.entry_seuil_haut_ajout, ""),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valeur)

        self._statut(
            f"{ticker} ajouté au portfolio ({quantite} action(s)).",
            "green",
        )

    def retirer_titre(self):
        selection = self._ticker_selectionne()

        if selection is None:
            self._statut(
                "Sélectionnez un titre à retirer.",
                "orange",
            )
            return

        _, ticker = selection

        self.portfolio.retirer_titre(ticker)

        if ticker in self.frames_prix:
            self.frames_prix.pop(ticker).destroy()

        self.labels_prix.pop(ticker, None)
        self.prix_observateurs.pop(ticker, None)

        self._statut(
            f"{ticker} retiré du portfolio.",
            "gray",
        )

    def modifier_selection(self):
        selection = self._ticker_selectionne()

        if selection is None:
            self._statut(
                "Sélectionnez un titre à modifier.",
                "orange",
            )
            return

        _, ticker = selection

        texte_qte = self.entry_nouvelle_quantite.get().strip()
        texte_bas = self.entry_nouveau_seuil_bas.get().strip()
        texte_haut = self.entry_nouveau_seuil_haut.get().strip()

        if not texte_qte and not texte_bas and not texte_haut:
            self._statut(
                "Entrez une nouvelle quantité et/ou de nouvelles alertes.",
                "orange",
            )
            return

        titre = self.portfolio.get_titre(ticker)
        donnees = titre.get_donnees()

        quantite = donnees["quantite"]
        seuil_bas = donnees["seuil_bas"]
        seuil_haut = donnees["seuil_haut"]

        try:
            if texte_qte:
                quantite = entier_positif(texte_qte)

            if texte_bas or texte_haut:
                if not (texte_bas and texte_haut):
                    self._statut(
                        "Les deux alertes doivent être fournies ensemble.",
                        "red",
                    )
                    return

                seuil_bas = flottant_positif(texte_bas)
                seuil_haut = flottant_positif(texte_haut)

                if seuil_bas >= seuil_haut:
                    self._statut(
                        "L'alerte basse doit être inférieure à l'alerte haute.",
                        "red",
                    )
                    return

        except ValueError:
            self._statut(
                "La quantité et les alertes doivent être des nombres positifs.",
                "red",
            )
            return

        titre.modifier(
            quantite,
            round(seuil_haut, 2),
            round(seuil_bas, 2),
        )

        self.portfolio.notifier()

        self.actualiser_liste(
            self.portfolio.get_donnees()["titres"]
        )

        for entry in (
            self.entry_nouvelle_quantite,
            self.entry_nouveau_seuil_bas,
            self.entry_nouveau_seuil_haut,
        ):
            entry.delete(0, tk.END)

        self._statut(
            f"{ticker} mis à jour.",
            "green",
        )

    def rafraichir(self):
        try:
            prix_actuels = {}

            for ticker in list(self.portfolio.get_titres()):
                prix, ouverture = recuperer_prix(ticker)

                prix_actuels[ticker] = {
                    "prix": prix,
                    "ouverture": ouverture,
                }

            self.portfolio.mise_a_jour(prix_actuels)

        except Exception as e:
            self.label_maj.config(
                text=f"Erreur lors du rafraîchissement : {e}",
                fg="red",
            )

        self.fenetre.after(
            INTERVALLE_MS,
            self.rafraichir,
        )

    def lancer(self):
        self.rafraichir()
        self.fenetre.mainloop()


if __name__ == "__main__":
    App().lancer()
