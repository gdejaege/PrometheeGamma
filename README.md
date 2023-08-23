# PROJ-H402 Promethee Gamma gui

The aim of this project is the realization of a graphic application allowing to visualize the results of the Promethee Gamma method.

## Poetry

The Python packaging and dependency management software poetry (https://python-poetry.org/) is used in this project. <br/>

So, you can install all dependancies with
```
poetry install
```

and, when you are in a terminal in the src directory,
```
cd src
```

you can run the project with
```
poetry run python main.py
```

If you don't want to use poetry, you can also install the dependencies and run the project without it. Please refer to the following.<br/>

## Third-party libraries

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