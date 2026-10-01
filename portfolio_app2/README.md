# Portfolio Tracker

Version séparée inspirée de `app2.py`.

## Installation

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Tkinter n'est pas une dépendance pip sous Windows : il est fourni avec Python.

## Lancement

```powershell
python main.py
```

## Organisation

- `main.py` : démarre l'application.
- `views/app.py` : interface Tkinter, yfinance et cycle de rafraîchissement.
- `models/portfolio.py` : sujet Observer contenant les titres.
- `models/titre.py` : sujet Observer représentant un titre.
- `observers/` : observateurs du portfolio et des titres.
- `portfolio.csv` : journal créé automatiquement pendant les rafraîchissements.

Le fichier `subject.py` peut rester celui fourni par l'enseignant.
Le fichier `observer.py` peut également être remplacé par celui fourni si celui-ci est l'interface officielle du projet.
