from observateurs.observateur import Observateur
import csv
from datetime import datetime




class Logger(Observateur):
    def __init__(self, portfolio, fichier="portfolio.csv"):
        self._portfolio = portfolio
        self._fichier = fichier

    def actualiser(self):
        titres = self._portfolio.get_donnees()["titres"]

        with open(
            self._fichier,
            "a",
            newline="",
            encoding="utf-8"
        ) as fichier:

            writer = csv.writer(fichier)

            for titre in titres.values():
                writer.writerow([
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    titre["ticker"],
                    titre["prix"],
                    titre["quantite"]
                ])