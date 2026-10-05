from modeles.sujet import Sujet

class Titre(Sujet):
    """Sujet représentant un titre boursier."""

    def __init__(self, ticker, quantite, seuil_haut, seuil_bas):
        self._observateurs = []
        self._ticker = ticker
        self._prix = 0.0
        self._ouverture = 0.0

    def abonner(self, observateur):
        if observateur not in self._observateurs:
            self._observateurs.append(observateur)

    def desabonner(self, observateur):
        if observateur in self._observateurs:
            self._observateurs.remove(observateur)

    def notifier(self):
        for observateur in self._observateurs:
            observateur.actualiser()

    def get_ticker(self):
        return self._ticker

    def get_donnees(self):
        return {
            "prix": self._prix,
            "ouverture": self._ouverture
        }

    def mettre_a_jour_prix(self, prix, ouverture):
        self._prix = prix
        self._ouverture = ouverture
        self.notifier()

    def modifier(self, quantite=None, seuil_haut=None, seuil_bas=None):
        if quantite is not None:
            self._quantite = quantite
        if seuil_haut is not None:
            self._seuil_haut = seuil_haut
        if seuil_bas is not None:
            self._seuil_bas = seuil_bas
        self.notifier()