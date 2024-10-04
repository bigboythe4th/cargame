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


# **Car Collection Game - ReadMe**

## **Overview**
This game is a car collecting and trading simulation where you can earn money, open boxes to collect cars, participate in drag races, complete achievements, and engage in trading. Your goal is to collect rare cars, upgrade your earnings, and build an ultimate car collection.

### **Getting Started**
1. **Launch the Game**: Once you've run the script, the game will start in full-screen mode.
2. **Main Menu**: In the main menu, you will see different options such as:
   - Open Boxes 20k each
   - View Inventory
   - Participate in Drag Races
   - Manage Safe Deposits
   - List a Car for Trade
   - Global Market for buying/selling cars
   - Play a Coinflip Game
   - Upgrade your click power for earning more money
   - View Achievements
   - Game Settings
   
### **How to Play**
1. **Earning Money**: Simply click anywhere on the main screen to earn money. Each click gives you a fixed amount, and you can upgrade this by purchasing the "Upgrade Click Power".
   
2. **Opening Boxes**:
   - Go to the **Boxes** section or just click on open box to buy and open different boxes.
   - Each box cost from 20K to 10M but the open box button will cost 20k for each car
   - Each box contains cars of varying rarities. The rarer the car, the faster and more valuable it will be.
   - Opening boxes costs money, so you need to have sufficient funds to unlock new cars.
   
3. **Drag Races**:
   - Select a car from your inventory and race against an opponent. The car with the higher speed wins.
   - Winning a race earns you money based on the car’s value, while losing will cost you.

4. **Safe Deposit**:
   - Use the **Safe** to store money or cars. Money in the safe generates interest over time.
   - You can deposit or withdraw money and cars between your inventory and the safe.

5. **Car Trading and Global Market**:
   - You can list cars for sale or trade them in the **Global Market**.
   - Buy or trade cars using trade offers from both bots and other players. Evaluate trade offers carefully to get the best deals.

6. **Achievements and Quests**:
   - Achievements are milestones like "Open 50 Boxes" or "Earn $1,000,000". Completing achievements gives you rewards.
   - Quests are smaller tasks such as "Collect 5 Cars" or "Win 3 Races".
   
7. **Upgrading**:
   - You can spend money to upgrade your click power, which increases the amount of money you earn per click.

### **Controls**
- **Mouse**: Use your mouse to navigate menus and click buttons.
- **Click**: Left-click to earn money or interact with the game menus.

### **Game Saving/Loading**:
- The game automatically saves progress when you exit or can be manually saved via the **Settings** menu.
- You can load saved progress from the **Settings** menu anytime.

### **Box Types and Rarity Probabilities**
- There are several types of boxes, each with different price points and car rarity probabilities. More expensive boxes offer better chances to get rare cars.
- Rarity levels include Common, Uncommon, Rare, Epic, Legendary, Mythical, and more.

### **Races Won and Inventory**:
- You can view your collection of cars, their speeds, and values in the **Inventory** section. The more rare the car, the higher its speed and value.

### **Additional Features**:
- **Sorting Options**: Sort your inventory by speed, rarity, or price to quickly find your best-performing cars.
- **Achievements Page**: Track your progress in unlocking achievements.

Enjoy building your ultimate car collection!
