from observateurs.observateur import Observateur
from datetime import datetime
import tkinter as tk

class MiseAJour(Observateur):

    def __init__(self, fenetre):
        self._label_maj = tk.Label(fenetre, text="", font=("Segoe UI", 9), fg="gray")
        self._label_maj.pack(pady=5)

    def actualiser(self):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.label_maj.config(text=f"Dernière mise à jour : {date}", fg="gray")