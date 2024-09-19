# Promethee Gamma gui

This application provides a user interface to the Promethee γ method developed in the article by Gilles DEJAEGERE and Yves DE SMET: "Promethee γ: a new Promethee based method for partial ranking based on valued coalitions of monocriterion net flow scores" (https://doi.org/10.1002/mcda.1805). <br/>

Researchers wanting to explore or use Promethee γ (related or not to this user interface) can contact Gilles DEJAEGERE for any question, request of help or collaboration.
Please feel free to contact him also for any other question related to the Promethee family of methods. <br/>

It displays the results in 3 different ways, as a matrix, as an orthogonal graph and as a ranking, while allowing the impact of the 3 parameters specific to the method to be visualized. The application also offers help in determining these 3 parameters, thanks to a small number of peer comparisons evaluated by the user.


## Documentation

You can find the html documentation in "./Docs/build/html". Please, open the index.html file in your browser to access to the documentation. <br/>


## Installation and running

A version superior to python3.11 is necessary for running this application.

### Third-party libraries


These libraries can be found in requirements.txt <br />

- customtkinter (https://github.com/TomSchimansky/CustomTkinter) for the widgets. <br />

Installation : 
```
pip install customtkinter
```

- matplotlib to make the orthogonal graph <br />

Installation : 
```
pip install matplotlib
```

- numpy <br />

Installation : 
```
pip install numpy
```

## How to run

The runnable file is the file main.py in the src directory. <br />

When you are in a terminal in the src directory, you can run it with
```
python3 main.py
```
