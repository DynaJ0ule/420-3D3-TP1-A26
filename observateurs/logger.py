from observateurs.observateur import Observateur
import csv
from datetime import datetime

class Logger(Observateur):

    def __init__(self, fichier="portfolio.csv"):
        self._fichier = fichier

    def actualiser(self, portfolio):
        titres = portfolio.get_donnees()["titres"]

        with open(
            self._fichier,
            "a",
            newline="",
            encoding="utf-8",
        ) as fichier:
            writer = csv.writer(fichier)

            for titre in titres.values():
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    titre["ticker"],
                    f'{titre["prix"]:.2f}',
                    f'{titre["ouverture"]:.2f}',
                ])
