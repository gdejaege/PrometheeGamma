# Avancement du projet

This file (in french) is used to indicate the progress of the project and any available features and their status. <br />


## Onglet "Data"

- Les données doiventent être entrées à partir d'un fichier source csv. Ensuite, elles peuvent être modifiées manuellement directement dans l'application grâce à un tableau d'entrée. <br />

- Ce tableau supporte l'ajout (et la suppression) de colonne (= de critère) et de ligne (= d'alternative). <br/>

### A ajouter:

- La possibilité de sauvegarder les modifications effectuées, c'est-à-dire créer un bouton "save" pour enregistrer le tableau au format csv. <br/>

- Eventuellement : la prise en charge d'autres format de fichier, tel que json. <br/>

- ... <br/>

### A modifier/améliorer:

- Les couleurs ? <br/>

- ... <br/>


## Onglet "Results"

- Les résultats peuvent être obtenu via le bouton "Obtain results". Ils sont alors affichés de trois manières différentes : sous forme de matrice dans une "textbox", dans un graphe orthogonal permettant de visualiser les proportions d'e préférence/indifférence/incomparabilité, 
ainsi que dans un shcéma montrant le classement en fonction de la préférence, ainsi que les liens d'indifférence et d'incomparabilité. <br/>

- Les entrées et les sliders permettent de modifier la valeur des 3 nouveaux paramètres de PROMETHEE Gamma. Ces modifications sont visibles en temps réel sur les résultats. <br/>

- Le bouton "Obtain results" devient "Reload results" après sa première activation. Il permet de recalculer les résultats après une modification des données dans l'onglet "Data". <br/>

### A ajouter

- ... <br/>

### A modifier/améliorer

- Le graphe orthogonal n'est pas tout à fait terminé (il manque la visualisation des thresholds). <br/>

- Dans la visualisation graphique, les traits montrant l'indifférence et l'incomparabilité peuvent se superposer, rendant le schéma illisible. Il faut donc encore l'améliorer. Possibilité de zoom et de déplacement à l'aide d'une "main" ? <br/>

- Les couleurs ? <br/>

- ... <br/>


## Code

- Le code est organisé selon le paradigme Model-View-Controller (MVC).

### A améliorer

- ...

### A ajouter

- modèles UML pour la compréhension du code


## TODO

- Possibilité d'enregistrer les résultats.

### Troisième onglet :

- afficher les questions une par une (et pas l'une à la suite de l'autre) (si choix des questions déterministique : question suivante peut être choisie en fonction de la réponse à la précédente)
- modularité -> différentes manière de déterminer les paramètres -> pouvoir appeler un autre code facilement
- déterminisme dans les valuers des paramètres en sortie -> tjrs les mêmes valeurs de paramètres pour les même données et les mêmes réponses aux questions -> essayer recherche (quasi) exhaustive avec pruning
- éventuellement -> ranges valables pour les paramètres