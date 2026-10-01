from datetime import datetime
from observers.observer import Observateur


class MiseAJour(Observateur):
    def __init__(self, callback):
        self._callback = callback

    def actualiser(self):
        maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._callback(maintenant)
