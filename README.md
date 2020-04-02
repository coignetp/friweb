# Informations générales
## Installation
Pour utiliser ce dépôt, il faut avoir Python version >= 3.5.  
Installer les dépendances avec `pip3 install -r requirements.txt`. **[TODO: compléter le requirements.txt]**  

Ce projet utilise tkinter pour avoir une interface graphique.

Le *dataset* doit être placé directement dans le dossier `data`, de façon à avoir les fichiers placés comme ceci : `data/0/3dradiology.stanford.edu_`

## Utilisation
### GUI
Pour utiliser ce projet avec la GUI, il suffit de lancer `python3 src/gui.py`.  
Il est à noter que lors de la première utilisation, l'index inversé va être crée ce qui prend quelques minutes.

Une fois la GUI lancée, il est possible de rechercher les fichiers du dataset dans la barre de recherche. Deux types de recherches sont disponibles :
* Booléenne : si la recherche ne contient pas de mot-clé booléen (`and`, `or`, `and not`), le mot-clé `and` sera rajouté entre chaque mot de la requête.
* Vectorielle

### Tests
Pour tester les recherches avec des requêtes d'exemple dans `queries/`, il est possible de faire `python3 src/test.py`.

**[TODO: expliquer l'output]**

# Détails des choix
## Index inversé
L'index inversé sauvegarde pour chaque mot du vocabulaire :
`MOT,3	0/admission.stanford.edu_counselors_counselor_mailing_list.html,1;1,	0/admission.stanford.edu_application_deadlines_fee.html,1;69,	0/cdc.stanford.edu_,1;112`.  
On a le mot de vocabulaire, le nombre de fichier contenant ce mot de vocabulaire, puis pour chaque fichier concerné son nom, le nombre d'occurence du mot dans le fichier et sa position.

**[TODO: lemmetize]**

**[TODO: compléter]**