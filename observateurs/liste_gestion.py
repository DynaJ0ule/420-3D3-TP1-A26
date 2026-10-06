from observateurs.observateur import Observateur


class ListeGestion(Observateur):

    def __init__(self, listbox):
        self._listbox = listbox

    def actualiser(self, sujet):
        titres = sujet.get_donnees()["titres"]

        self._listbox.delete(0, "end")

        for ticker, titre in titres.items():
            texte = f"{ticker} : {titre['quantite']} actions"
            self._listbox.insert("end", texte)

