# cargame

## Setup dev environment

Before you can play the game, install the dependencies:
```
pip install dearpygui
pip install pygame
```

## Start the game

To play the game, run:
```
python main.py
```

## Quickstart

Quickstart:
- Open the settings menu and chose "Load Game"
- Go back to the main menu then chose "Drag Race"
- Choose a car in the next screen
- Watch your car in the simulated race
- ????
- Profit!!

## Building the exe 

We build the exe with the package cx-Freeze. 

Install it:
```
pip install cx-Freeze
```

Build the exe:
```
python setup.py build
```

Run the exe:
```
build\{platform}\main.exe
```
