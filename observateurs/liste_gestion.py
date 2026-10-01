from observateurs.observateur import Observateur



class ListeGestion(Observateur):
    def __init__(self, portfolio, callback):
        self._portfolio = portfolio
        self._callback = callback

    def actualiser(self):
        donnees = self._portfolio.get_donnees()

        self._callback(
            donnees["titres"]
        )