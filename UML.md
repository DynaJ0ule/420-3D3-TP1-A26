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
	class Titre{
		- _tricker: str
		- _prix: float
		- _ouverture: float
		- _quantitee: int
		- _seuil-haut: float
		- _seuil-bas: float
		+ abonner()
		+ desabonner()
		+ notifier()
		+ get_donnees(): dict
		+ mettre_a_jour_prix(prix:float)
		+ modifier()
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
liste gestion est fake, c'est juste le dashboard? Sauf la listbox? Il faut qu'elle puisse donner sa sélection somehow.
