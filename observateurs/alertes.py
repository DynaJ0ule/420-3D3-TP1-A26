from observateurs.observateur import Observateur


class Alertes(Observateur):

    def __init__(self, portfolio, callback):
        self._portfolio = portfolio
        self._callback = callback

    def actualiser(self):
        donnees = self._portfolio.get_donnees()
        titres = donnees["titres"]

        alertes = []

        for ticker, titre in titres.items():

            # Les données du titre
            prix = titre["prix"]
            seuil_haut = titre["seuil_haut"]
            seuil_bas = titre["seuil_bas"]
            if prix <= 0:
                continue

            if prix >= seuil_haut:
                alertes.append(
                    f"⚠️ {ticker} dépasse le seuil haut "
                    f"({prix:.2f} $ ≥ {seuil_haut:.2f} $)"
                )

            elif prix <= seuil_bas:
                alertes.append(
                    f"⚠️ {ticker} sous le seuil bas "
                    f"({prix:.2f} $ ≤ {seuil_bas:.2f} $)"
                )

        self._callback(alertes)