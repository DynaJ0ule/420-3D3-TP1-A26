from observateurs.observateur import Observateur



class PrixTempsReel(Observateur):
    def __init__(self, titre, callback):
        self._titre = titre
        self._callback = callback

    def actualiser(self):
        donnees = self._titre.get_donnees()
        prix = donnees["prix"]
        ouverture = donnees["ouverture"]

        if ouverture:
            variation = (prix - ouverture) / ouverture * 100
        else:
            variation = 0

        self._callback(donnees["ticker"], prix, variation)
