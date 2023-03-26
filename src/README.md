# Avancement du projet

This file (in french) is used to indicate the progress of the project and any available features and their status. <br />


## Onglet "Data"

- Les données doiventent être entrées à partir d'un fichier source csv. Ensuite, elles peuvent être modifiées manuellement directement dans l'application grâce à un tableau d'entrée. <br />

- Ce tableau supporte l'ajout (et la suppression) de colonne (= de critère) et de ligne (= d'alternative). <br/>

### A ajouter:

- Des informations à propos de la fonction de préférence des critères et de ses paramètres. Pouvoir visualiser cette fonction de préférence. <br/>

- Des types de fonctions de préférence supplémentaire (pour le moment, seuls deux sont prises en charge, l'usuelle et la linéaire). <br/>

- La possibilité de sauvegarder les modifications effectuées, c'est-à-dire créer un bouton "save" pour enregistrer le tableau au format csv. <br/>

- Eventuellement : la prise en charge d'autres format de fichier, tel que json. <br/>

- ... <br/>

### A modifier/améliorer:

- Pouvoir changer de fichier source. Actuellement, il faut relancer l'application pour pouvoir l'utiliser sur d'autres données. Le chargement d'un second fichier source provoque un bug. <br/>

- Les couleurs ? <br/>

- ... <br/>


## Onglet "Results"

- Les résultats peuvent être obtenu via le bouton "Obtain results". Ils sont alors afficher sous forme de matrice dans une "textbox". <br/>

- Les entrées et les sliders permettent de modifier la valeur des 3 nouveaux paramètres de PROMETHEE Gamma. Ces modifications sont visibles en temps réel sur les résultats. <br/>

- Le bouton "Obtain results" devient "Reload results" après sa première activation. Il permet de recalculer les résultats après une modification des données dans l'onglet "Data". <br/>

- Les boutons "See orthogonal graph" et "See graphical results" permettent d'afficher les résultats de manière graphique. <br/>

### A ajouter

- ... <br/>

### A modifier/améliorer

- Le processus d'obtention et d'affichage des résultat n'est pas optimal. Il peut provoquer des latences lorsque de nombreux recalculs sont demandés lors de l'utilisation des sliders. Il faut encore optimiser tout cela. <br/>

- Le graphe orthogonal n'est pas tout à fait terminé (il manque la visualisation des thresholds). <br/>

- Dans la visualisation graphique, les traits montrant l'indifférence et l'incomparabilité peuvent se superposer, rendant le schéma illisible. Il faut donc encore l'améliorer. Possibilité de zoom et de déplacement à l'aide d'une "main" ? <br/>

- Les couleurs ? <br/>

- ... <br/>


## Code

- Le code est organisé en classe selon le principe de l'orienté objet et commenté.

### A améliorer

- Le code doit être simplifié à certain endroit, et certain commentaires doivent encore être complétés/ajoutés.

- ...



## TODO

- Possibilité d'enregistrer les résultats.

- Troisième onglet : aide au choix des paramètres

- refactoring + schema explicatif code (Modelisation UML)