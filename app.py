import tkinter as tk
import yfinance as yf
from datetime import datetime


# Configuration du portfolio
TITRES = {
    "AAPL":  {"quantite": 10, "seuil_haut": 200.0, "seuil_bas": 150.0},
    "GOOGL": {"quantite": 5,  "seuil_haut": 160.0, "seuil_bas": 120.0},
    "MSFT":  {"quantite": 8,  "seuil_haut": 430.0, "seuil_bas": 380.0},
}

INTERVALLE_MS = 30000  # 30 secondes


class App:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Portfolio Tracker")
        self.fenetre.resizable(False, False)

        self.prix_precedents = {ticker: None for ticker in TITRES}

        # Titre
        tk.Label(
            self.fenetre,
            text="Portfolio Tracker",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Affichage des prix
        self.frame_prix = tk.LabelFrame(
            self.fenetre, text="Prix en temps réel", padx=10, pady=10
        )
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)

        self.labels_prix = {}
        self.frames_prix = {}
        for ticker in TITRES:
            self._creer_ligne_prix(ticker)

        # Gestion des titres (ajout / retrait)
        frame_gestion = tk.LabelFrame(
            self.fenetre, text="Gérer les titres", padx=10, pady=10
        )
        frame_gestion.pack(fill=tk.X, padx=10, pady=5)

        frame_ajout = tk.Frame(frame_gestion)
        frame_ajout.pack(fill=tk.X)
        self.entry_ticker = tk.Entry(frame_ajout, width=10)
        self.entry_ticker.pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(frame_ajout, text="Qté:").pack(side=tk.LEFT)
        self.entry_quantite = tk.Entry(frame_ajout, width=5)
        self.entry_quantite.insert(0, "1")
        self.entry_quantite.pack(side=tk.LEFT, padx=(2, 5))
        tk.Label(frame_ajout, text="Alerte basse:").pack(side=tk.LEFT)
        self.entry_seuil_bas_ajout = tk.Entry(frame_ajout, width=7)
        self.entry_seuil_bas_ajout.pack(side=tk.LEFT, padx=(2, 5))
        tk.Label(frame_ajout, text="Alerte haute:").pack(side=tk.LEFT)
        self.entry_seuil_haut_ajout = tk.Entry(frame_ajout, width=7)
        self.entry_seuil_haut_ajout.pack(side=tk.LEFT, padx=(2, 5))
        tk.Button(
            frame_ajout, text="Ajouter", command=self.ajouter_titre
        ).pack(side=tk.LEFT)
        tk.Label(
            frame_gestion,
            text="(Alertes optionnelles à l'ajout : si vides, calculées à ±20% du prix actuel)",
            font=("Arial", 8), fg="gray"
        ).pack(anchor="w")

        frame_liste = tk.Frame(frame_gestion)
        frame_liste.pack(fill=tk.X, pady=(5, 0))
        self.listbox_titres = tk.Listbox(frame_liste, height=4, exportselection=False)
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.X, expand=True)
        for ticker in TITRES:
            self.listbox_titres.insert(tk.END, self._texte_listbox(ticker))
        tk.Button(
            frame_liste, text="Retirer", command=self.retirer_titre
        ).pack(side=tk.LEFT, padx=(5, 0), anchor="n")

        frame_modif = tk.Frame(frame_gestion)
        frame_modif.pack(fill=tk.X, pady=(5, 0))
        tk.Label(frame_modif, text="Nouvelle quantité:").pack(side=tk.LEFT)
        self.entry_nouvelle_quantite = tk.Entry(frame_modif, width=5)
        self.entry_nouvelle_quantite.pack(side=tk.LEFT, padx=(5, 5))
        tk.Button(
            frame_modif, text="Modifier", command=self.modifier_quantite
        ).pack(side=tk.LEFT)

        frame_modif_seuils = tk.Frame(frame_gestion)
        frame_modif_seuils.pack(fill=tk.X, pady=(5, 0))
        tk.Label(frame_modif_seuils, text="Alerte basse:").pack(side=tk.LEFT)
        self.entry_nouveau_seuil_bas = tk.Entry(frame_modif_seuils, width=7)
        self.entry_nouveau_seuil_bas.pack(side=tk.LEFT, padx=(5, 5))
        tk.Label(frame_modif_seuils, text="Alerte haute:").pack(side=tk.LEFT)
        self.entry_nouveau_seuil_haut = tk.Entry(frame_modif_seuils, width=7)
        self.entry_nouveau_seuil_haut.pack(side=tk.LEFT, padx=(5, 5))
        tk.Button(
            frame_modif_seuils, text="Modifier alertes", command=self.modifier_seuils
        ).pack(side=tk.LEFT)

        self.label_statut_titres = tk.Label(
            frame_gestion, text="", font=("Arial", 9), fg="gray"
        )
        self.label_statut_titres.pack(anchor="w", pady=(5, 0))

        # Valeur du portfolio
        frame_portfolio = tk.LabelFrame(
            self.fenetre, text="Mon portfolio", padx=10, pady=10
        )
        frame_portfolio.pack(fill=tk.X, padx=10, pady=5)

        self.label_valeur = tk.Label(
            frame_portfolio,
            text="Valeur totale : calcul en cours...",
            font=("Arial", 14, "bold")
        )
        self.label_valeur.pack()

        self.label_variation = tk.Label(
            frame_portfolio,
            text="",
            font=("Arial", 11)
        )
        self.label_variation.pack()

        # Alertes
        frame_alertes = tk.LabelFrame(
            self.fenetre, text="Alertes", padx=10, pady=10
        )
        frame_alertes.pack(fill=tk.X, padx=10, pady=5)

        self.label_alertes = tk.Label(
            frame_alertes,
            text="Aucune alerte",
            font=("Arial", 11),
            fg="gray",
            justify=tk.LEFT,
            wraplength=380
        )
        self.label_alertes.pack(anchor="w")

        # Dernière mise à jour
        self.label_maj = tk.Label(
            self.fenetre,
            text="",
            font=("Arial", 9),
            fg="gray"
        )
        self.label_maj.pack(pady=5)

        self.rafraichir()
        self.fenetre.mainloop()

    def _creer_ligne_prix(self, ticker):
        """Crée (ou recrée) la ligne d'affichage du prix pour un ticker."""
        frame = tk.Frame(self.frame_prix)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=f"{ticker}:", width=8,
                 font=("Arial", 12, "bold"), anchor="w").pack(side=tk.LEFT)
        label = tk.Label(frame, text="Chargement...", font=("Arial", 12))
        label.pack(side=tk.LEFT)
        self.labels_prix[ticker] = label
        self.frames_prix[ticker] = frame

    def _texte_listbox(self, ticker):
        infos = TITRES[ticker]
        return (
            f"{ticker} — {infos['quantite']} action(s) "
            f"(alerte : {infos['seuil_bas']:.2f} $ / {infos['seuil_haut']:.2f} $)"
        )

    def _ticker_selectionne(self):
        selection = self.listbox_titres.curselection()
        if not selection:
            return None
        texte = self.listbox_titres.get(selection[0])
        return selection[0], texte.split(" — ")[0]

    def ajouter_titre(self):
        ticker = self.entry_ticker.get().strip().upper()
        if not ticker:
            return

        if ticker in TITRES:
            self.label_statut_titres.config(
                text=f"{ticker} est déjà dans le portfolio.", fg="orange"
            )
            return

        try:
            quantite = int(self.entry_quantite.get().strip())
            if quantite <= 0:
                raise ValueError("quantité invalide")
        except ValueError:
            self.label_statut_titres.config(
                text="La quantité doit être un nombre entier positif.", fg="red"
            )
            return

        texte_seuil_bas = self.entry_seuil_bas_ajout.get().strip()
        texte_seuil_haut = self.entry_seuil_haut_ajout.get().strip()
        try:
            seuil_bas = float(texte_seuil_bas) if texte_seuil_bas else None
            seuil_haut = float(texte_seuil_haut) if texte_seuil_haut else None
            if (seuil_bas is not None and seuil_bas <= 0) or (
                seuil_haut is not None and seuil_haut <= 0
            ):
                raise ValueError("seuil invalide")
            if seuil_bas is not None and seuil_haut is not None and seuil_bas >= seuil_haut:
                self.label_statut_titres.config(
                    text="L'alerte basse doit être inférieure à l'alerte haute.", fg="red"
                )
                return
        except ValueError:
            self.label_statut_titres.config(
                text="Les alertes doivent être des nombres positifs.", fg="red"
            )
            return

        try:
            info = yf.Ticker(ticker).fast_info
            prix = info['last_price']
            ouverture = info['open']
            if prix is None:
                raise ValueError("titre introuvable")
        except Exception:
            self.label_statut_titres.config(
                text=f"Le titre '{ticker}' n'existe pas.", fg="red"
            )
            return

        # Ajout au portfolio ; seuils fournis par l'utilisateur, sinon ±20% du prix actuel
        TITRES[ticker] = {
            "quantite": quantite,
            "seuil_haut": round(seuil_haut if seuil_haut is not None else prix * 1.2, 2),
            "seuil_bas": round(seuil_bas if seuil_bas is not None else prix * 0.8, 2),
        }
        self.prix_precedents[ticker] = None

        self._creer_ligne_prix(ticker)
        self.listbox_titres.insert(tk.END, self._texte_listbox(ticker))
        self.entry_ticker.delete(0, tk.END)
        self.entry_quantite.delete(0, tk.END)
        self.entry_quantite.insert(0, "1")
        self.entry_seuil_bas_ajout.delete(0, tk.END)
        self.entry_seuil_haut_ajout.delete(0, tk.END)

        # Affichage immédiat du prix récupéré, sans attendre le prochain cycle
        variation = ((prix - ouverture) / ouverture) * 100
        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"
        self.labels_prix[ticker].config(
            text=f"{prix:.2f} $  {symbole} {abs(variation):.2f}%", fg=couleur
        )

        self.label_statut_titres.config(
            text=f"{ticker} ajouté au portfolio ({quantite} action(s)).", fg="green"
        )

    def retirer_titre(self):
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self.label_statut_titres.config(
                text="Sélectionnez un titre à retirer.", fg="orange"
            )
            return
        index, ticker = selectionne

        self.listbox_titres.delete(index)

        del TITRES[ticker]
        self.prix_precedents.pop(ticker, None)
        self.labels_prix.pop(ticker, None)
        frame = self.frames_prix.pop(ticker, None)
        if frame is not None:
            frame.destroy()

        self.label_statut_titres.config(
            text=f"{ticker} retiré du portfolio.", fg="gray"
        )

    def modifier_quantite(self):
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self.label_statut_titres.config(
                text="Sélectionnez un titre à modifier.", fg="orange"
            )
            return
        index, ticker = selectionne

        try:
            nouvelle_quantite = int(self.entry_nouvelle_quantite.get().strip())
            if nouvelle_quantite <= 0:
                raise ValueError("quantité invalide")
        except ValueError:
            self.label_statut_titres.config(
                text="La quantité doit être un nombre entier positif.", fg="red"
            )
            return

        TITRES[ticker]['quantite'] = nouvelle_quantite
        self.listbox_titres.delete(index)
        self.listbox_titres.insert(index, self._texte_listbox(ticker))
        self.listbox_titres.selection_set(index)
        self.entry_nouvelle_quantite.delete(0, tk.END)

        self.label_statut_titres.config(
            text=f"Quantité de {ticker} mise à jour : {nouvelle_quantite} action(s).",
            fg="green"
        )

    def modifier_seuils(self):
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self.label_statut_titres.config(
                text="Sélectionnez un titre à modifier.", fg="orange"
            )
            return
        index, ticker = selectionne

        try:
            nouveau_seuil_bas = float(self.entry_nouveau_seuil_bas.get().strip())
            nouveau_seuil_haut = float(self.entry_nouveau_seuil_haut.get().strip())
            if nouveau_seuil_bas <= 0 or nouveau_seuil_haut <= 0:
                raise ValueError("seuil invalide")
            if nouveau_seuil_bas >= nouveau_seuil_haut:
                self.label_statut_titres.config(
                    text="L'alerte basse doit être inférieure à l'alerte haute.", fg="red"
                )
                return
        except ValueError:
            self.label_statut_titres.config(
                text="Les alertes doivent être des nombres positifs.", fg="red"
            )
            return

        TITRES[ticker]['seuil_bas'] = round(nouveau_seuil_bas, 2)
        TITRES[ticker]['seuil_haut'] = round(nouveau_seuil_haut, 2)
        self.listbox_titres.delete(index)
        self.listbox_titres.insert(index, self._texte_listbox(ticker))
        self.listbox_titres.selection_set(index)
        self.entry_nouveau_seuil_bas.delete(0, tk.END)
        self.entry_nouveau_seuil_haut.delete(0, tk.END)

        self.label_statut_titres.config(
            text=f"Alertes de {ticker} mises à jour : "
                 f"{nouveau_seuil_bas:.2f} $ / {nouveau_seuil_haut:.2f} $.",
            fg="green"
        )

    def rafraichir(self):
        try:
            # Récupérer les prix via yfinance
            prix_actuels = {}
            for ticker in TITRES:
                info = yf.Ticker(ticker).fast_info
                prix_actuels[ticker] = {
                    'prix': info['last_price'],
                    'ouverture': info['open'],
                }

            # Mettre à jour les labels de prix
            for ticker, donnees in prix_actuels.items():
                prix = donnees['prix']
                ouverture = donnees['ouverture']
                variation = ((prix - ouverture) / ouverture) * 100
                symbole = "▲" if variation >= 0 else "▼"
                couleur = "green" if variation >= 0 else "red"
                texte = f"{prix:.2f} $  {symbole} {abs(variation):.2f}%"
                self.labels_prix[ticker].config(text=texte, fg=couleur)

            # Mettre à jour la valeur du portfolio
            valeur_totale = sum(
                prix_actuels[t]['prix'] * TITRES[t]['quantite']
                for t in TITRES
            )
            self.label_valeur.config(
                text=f"Valeur totale : {valeur_totale:.2f} $"
            )

            # Calculer la variation de la valeur du portfolio
            valeur_ouverture = sum(
                prix_actuels[t]['ouverture'] * TITRES[t]['quantite']
                for t in TITRES
            )
            variation_portfolio = valeur_totale - valeur_ouverture
            couleur_variation = "green" if variation_portfolio >= 0 else "red"
            symbole = "▲" if variation_portfolio >= 0 else "▼"
            self.label_variation.config(
                text=f"{symbole} {abs(variation_portfolio):.2f} $ depuis l'ouverture",
                fg=couleur_variation
            )

            # Vérifier les alertes
            alertes = []
            for ticker, donnees in prix_actuels.items():
                prix = donnees['prix']
                if prix >= TITRES[ticker]['seuil_haut']:
                    alertes.append(
                        f"⚠️ {ticker} dépasse le seuil haut "
                        f"({prix:.2f} $ ≥ {TITRES[ticker]['seuil_haut']:.2f} $)"
                    )
                elif prix <= TITRES[ticker]['seuil_bas']:
                    alertes.append(
                        f"⚠️ {ticker} sous le seuil bas "
                        f"({prix:.2f} $ ≤ {TITRES[ticker]['seuil_bas']:.2f} $)"
                    )

            if alertes:
                self.label_alertes.config(
                    text="\n".join(alertes), fg="red"
                )
            else:
                self.label_alertes.config(text="Aucune alerte", fg="gray")

            # Écrire dans le fichier log CSV
            horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("portfolio.csv", 'a') as f:
                for ticker, donnees in prix_actuels.items():
                    f.write(
                        f"{horodatage},{ticker},"
                        f"{donnees['prix']:.2f},"
                        f"{donnees['ouverture']:.2f}\n"
                    )

            # Mettre à jour l'horodatage
            self.label_maj.config(
                text=f"Dernière mise à jour : {horodatage}"
            )

            self.prix_precedents = prix_actuels

        except Exception as e:
            self.label_maj.config(text=f"Erreur : {e}", fg="red")

        self.fenetre.after(INTERVALLE_MS, self.rafraichir)


if __name__ == "__main__":
    app = App()
