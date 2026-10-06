from modeles.sujet import Sujet
from modeles.titre import Titre

class Portfolio(Sujet):
    def __init__(self):
        self._observateurs = []
        self._titres = {} #ticker: str : {titre :Titre , quantite: int, seuil_haut: float, seuil_bas: float}

    def abonner(self, observateur):
        if observateur not in self._observateurs:
            self._observateurs.append(observateur)

    def desabonner(self, observateur):
        if observateur in self._observateurs:
            self._observateurs.remove(observateur)

    def notifier(self):
        for observateur in self._observateurs:
            observateur.actualiser(self)

    def get_donnees(self):
        return {
        "titres": {
            ticker: titre.get_donnees()
            for ticker, titre in self._titres.items()
        }
        }
        

    def ajouter_titre( self, ticker, quantite, seuil_haut, seuil_bas ): 
        if ticker in self._titres: 
            raise ValueError( f"Le titre {ticker} existe déjà." ) 
        titre = Titre( ticker, quantite, seuil_haut, seuil_bas ) 
        self._titres[ticker] = titre
        self.notifier()

    def modifier_titre(self,ticker,quantite=None,seuil_haut=None,seuil_bas=None):
        if ticker not in self._titres:
            raise ValueError(
            f"Le titre {ticker} n'existe pas dans le portfolio."
            )

        self._titres[ticker].modifier(
        quantite,
        seuil_haut,
        seuil_bas
         )

        self.notifier()
    def retirer_titre(self, ticker):
        if ticker in self._titres:
            del self._titres[ticker]
            self.notifier()

    def mise_a_jour(self, prix_actuels):
        for ticker, donnees in prix_actuels.items():
            if ticker in self._titres:
                self._titres[ticker].mettre_a_jour_prix(
                    donnees["prix"],
                    donnees["ouverture"]
                )

        self.notifier()

    def get_titre(self, ticker):
        return self._titres.get(ticker)

    def get_titres(self):
        return self._titres