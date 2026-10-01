from observateurs.observateur import Observateur
class Alertes(Observateur):
    def __init__(self, portfolio, callback):
        self._portfolio = portfolio
        self._callback = callback

    def actualiser(self):
        titres = self._portfolio.get_donnees()["titres"]

        alertes = []

        for titre in titres.values():
            ticker = titre["ticker"]
            prix = titre["prix"]
            seuil_haut = titre["seuil_haut"]
            seuil_bas = titre["seuil_bas"]

            if prix >= seuil_haut:
                alertes.append(
                    f"{ticker} a dépassé le seuil haut : "
                    f"{prix:.2f} $"
                )

            elif prix <= seuil_bas:
                alertes.append(
                    f"{ticker} a dépassé le seuil bas : "
                    f"{prix:.2f} $"
                )

        self._callback(alertes)