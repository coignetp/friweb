# Informations générales

## Installation

Pour utiliser ce dépôt, il faut avoir Python version >= 3.5.  
Installer les dépendances avec `pip3 install -r requirements.txt`. **[TODO: compléter le requirements.txt]**

Ce projet utilise tkinter pour avoir une interface graphique.

Le _dataset_ doit être placé directement dans le dossier `data`, de façon à avoir les fichiers placés comme ceci : `data/0/3dradiology.stanford.edu_`

## Utilisation

### GUI

Pour utiliser ce projet avec la GUI, il suffit de lancer `python3 src/gui.py`.  
Il est à noter que lors de la première utilisation, l'index inversé va être crée ce qui prend quelques minutes.

Une fois la GUI lancée, il est possible de rechercher les fichiers du dataset dans la barre de recherche. Deux types de recherches sont disponibles :

- Booléenne : si la recherche ne contient pas de mot-clé booléen (`and`, `or`, `and not`), le mot-clé `and` sera rajouté entre chaque mot de la requête.
- Vectorielle

### Tests

Pour tester les recherches avec des requêtes d'exemple dans `queries/`, il est possible de faire `python3 src/test.py`.

#### Format du fichier de test

Pour rajouter des cas au test, il suffit de rajouter la requête au fichier `queries/queries.txt` en respectant le formalisme suivant:

- une première ligne contenant la query
- une seconde ligne avec le lien vers le fichier d'output correspondant (chemin absolu ou elatif **à partir de la racine du projet**. ex: `queries/ouput/1.out`)

#### Résultats

Le résultat pour chaque query se présente sous cette forme :

```
Requête : stanford computer science
Modèle : Vectoriel
Précision : 0.05759625461028621
Rappel : 1.0
Requête : stanford computer science
Modèle : Boolean
Précision : 0.9988199197545433
Rappel : 1.0
```

Cela permet d'obtenir rapidement les deux métriques principales pour chaque modèle : la précision ($\frac{\text{nombre de documents pertinents retournés}}{\text{nombre de documents retournés}}$) et le rappel ($\frac{\text{nombre de documents pertinents retournés}}{\text{nombre de documents pertinents}}$).

# Détails des choix

## Index inversé

L'index inversé sauvegarde pour chaque mot du vocabulaire :
`MOT,3 0/admission.stanford.edu_counselors_counselor_mailing_list.html,1;1, 0/admission.stanford.edu_application_deadlines_fee.html,1;69, 0/cdc.stanford.edu_,1;112`.  
On a le mot de vocabulaire, le nombre de fichier contenant ce mot de vocabulaire, puis pour chaque fichier concerné son nom, le nombre d'occurence du mot dans le fichier et sa position.

**[TODO: lemmetize]**

**[TODO: compléter]**

## Modèle vectoriel

### Pourquoi un modèle vectoriel ?

Nous avons choisi d'implémenter un modèle vectoriel car ce modèle permet d'exprimer les requêtes dans un langage beaucoup plus proche du langage naturel. De plus, celui-ci permet donner un poids différent aux termes de la requête, notamment en faisant un tf-idf sur ceux-ci. Enfin, le modèle vectoriel renvoie un résultat scoré et trié ce que permet d'afficher en priorité le résultat qui semblent les plus pertinents. Cela facilite grandement le travail de recherche.

### Pourquoi de si mauvaises performances ?

Malgré de nombreuses tentatives pour améliorer les performances de notre modèle vectoriel celui garde des performances faibles (sur les requêtes de test) en comparaison à notre modèle booléen.

Ce que l'on peut voir, si l'on trace l'histogramme de nos scores (non normalisés), c'est qu'on a plusieurs "clusters" distribués suivant une loi normale et une barre proche de 0. Nous avons donc essayé de sélectionner ces clusters pour retourner seulement les résultats pertinents, mais la précision n en était pas améliorée, comparé à un simple filtre sur la liste pour supprime la bande 0. C'est pour cela que nous avons conservé ce filtre dans notre version final car nos tentives précédentes ralentissaient la requête.
![Histogramme](./misc/stanford_students.png)

Comment peut-on expliquer ces performances:

- les requêtes d'exemple utilisent beaucoup de mots considérés comme stop words (a, the, very ...) ce qui rend compliqué d'avoir une bonne précision.
- les requêtes d'exemples sont très générale et ne permettent pas de tester la spécificité de la collection. Par, le mot stanford revient très souvent, ce qui n'est pas très pertinent pour une collection venant de stanford.
- Enfin, ces requêtes font à l'origine partie d'un cours de stanford (CS276) et sont utilisés pour tester uniquement un modèle booléen, le modèle vectoriel n'ayant pas encore été abordé dans le cours. Ainsi, il semble logique que le modèle booléen ait de meilleures performances. Enfin, il nous semble que ces requêtes de test ne sont pas le résultat d'une analyse de la collection mais seulement le résultat d'un modèle booléen utilisé par le professeur. Ce pourrait expliquer les mauvaises performances du modèle vectoriel car celui-ci accorde une plus grande part à la pondération entre les différents termes.
