from observateurs.observateur import Observateur
class TableauDeBord(Observateur):
    def __init__(self, portfolio, callback):
        self._portfolio = portfolio
        self._callback = callback

    def actualiser(self):
        titres = self._portfolio.get_donnees()["titres"]

        nombre_titres = len(titres)
        quantite_totale = sum(
            titre["quantite"]
            for titre in titres.values()
        )

        self._callback(nombre_titres, quantite_totale)
