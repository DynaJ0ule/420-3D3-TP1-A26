from observateurs.observateur import Observateur
import tkinter as tk

class ListeGestion(Observateur):
    def __init__(self, parent):
        ligne_liste = tk.Frame(parent)
        ligne_liste.pack(fill=tk.X)
        self.listbox_titres = tk.Listbox(ligne_liste, height=4, exportselection=False)
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.X, expand=True)
        for ticker in TITRES:
            self.listbox_titres.insert(tk.END, self._texte_listbox(ticker))
        

    def actualiser(self, sujet):
        titres = sujet.get_donnees()["titres"]
        self._callback(titres)