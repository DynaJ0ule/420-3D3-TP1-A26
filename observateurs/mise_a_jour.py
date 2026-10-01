from observateurs.observateur import Observateur

from datetime import datetime



class MiseAJour(Observateur):
    def __init__(self, callback):
        self._callback = callback

    def actualiser(self):
        maintenant = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self._callback(maintenant)