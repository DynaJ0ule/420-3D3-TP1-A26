```mermaid
classDiagram
	class Sujet{
		<<interface>>
		- _observateurs : list
		+ abonner(observateur)
		+ desabonner(observateur)
		+ notifier()
		+ get_donnees() dict
	}
	class Observateur{
		<<interface>>
		+actualiser(sujet)
	}
	class PrixTempsReel{
		+actualiser(sujet)
	}
	class ListeGestion{
		+actualiser(sujet)
		+ticker_selectione() -> str
	}
	class Total{
		+actualiser(sujet)
	}
	class Alertes{
		+actualiser(sujet)
	}
	class MiseAJour{
		+actualiser(sujet)
	}
	class Logger{
		+actualiser(sujet)
	}
	class Dashboard{
		-_champ() -> tkinter.Entry
	}
	class Portfolio{
		- _titres: dict
		+ ajouter_titre()
		+ modifier_titre()
		+ retirer_titre()
		+ mise_a_jour()
	}
	Observateur <|.. PrixTempsReel
	Observateur <|.. ListeGestion
	Observateur <|.. Total
	Observateur <|.. Alertes
	Observateur <|.. MiseAJour
	Observateur <|.. Logger
	Sujet <|.. Portfolio
	
```
un autres sujet pour les titres peut-être?