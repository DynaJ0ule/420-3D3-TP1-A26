from observateurs.observateur import Observateur
class Total(Observateur):
    def __init__(self, portfolio, callback):
        self._portfolio = portfolio
        self._callback = callback

    def actualiser(self):
        titres = self._portfolio.get_donnees()["titres"]

        total = 0
        valeur_ouverture = 0

        for titre in titres.values():
            total += titre["prix"] * titre["quantite"]
            valeur_ouverture += (
                titre["ouverture"] * titre["quantite"]
            )

        if valeur_ouverture != 0:
            variation = (
                (total - valeur_ouverture)
                / valeur_ouverture
            ) * 100
        else:
            variation = 0

        self._callback(total, variation)