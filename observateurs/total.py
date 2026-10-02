from observateurs.observateur import Observateur
class Total(Observateur):
    def __init__(self, portfolio, callback):
        self._portfolio = portfolio
        self._callback = callback

    def actualiser(self):
        titres = self._portfolio.get_donnees()["titres"]

        total = sum(
            titre["prix"] * titre["quantite"]
            for titre in titres.values()
        )

        valeur_ouverture = sum(
            titre["ouverture"] * titre["quantite"]
            for titre in titres.values()
        )

        variation = (
            (total - valeur_ouverture) / valeur_ouverture * 100
            if valeur_ouverture
            else 0
        )

        self._callback(total, variation)