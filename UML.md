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
		+actualiser()
	}
	class PrixTempsReel
	class ListeGestion{
	- _portfolio: Portfolio
	+ actualiser()
	}
	class Total
	class Alertes
	class MiseAJour
	class Logger
	class TableauDeBord
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
