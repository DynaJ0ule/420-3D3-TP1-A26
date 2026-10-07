from observateurs.observateur import Observateur


class ListeGestion(Observateur):
    def __init__(self, parent):
        # (la sélection dans cette liste sert aussi au formulaire de modification)
        ligne_liste = tk.Frame(parent)
        ligne_liste.pack(fill=tk.X)
        self.listbox_titres = tk.Listbox(ligne_liste, height=4, exportselection=False)
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(ligne_liste, text="Retirer", command=self.retirer_titre).pack(side=tk.LEFT, padx=(5, 0), anchor="n")


    def actualiser(self, sujet):
        for ticker in sujet.titres:
                    self.listbox_titres.insert(tk.END, self._texte_listbox(ticker))
        titres = self._portfolio.get_donnees()["titres"]

    
    def ticker_selectionne(self):
        """Retourne (index, ticker) du titre sélectionné dans la liste, ou None.
        Le ticker est extrait du texte affiché (avant le tiret "—")."""
        selection = self.listbox_titres.curselection()
        if not selection:
            return None
        texte = self.listbox_titres.get(selection[0])
        return selection[0], texte.split(" — ")[0]
