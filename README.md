# Ornament Collector

## How to Play
The goal of the game is to get as high of a score as possible, and you get that by collecting all ornaments in a level while avoiding enemies, which are stars. You move by holding and dragging your character in the opposite direction of where you want to go, similar to a golf game. As you collect ornaments, a christmas tree will be filled, and once you get 5, 100 coins will be awarded to you, which you can use to upgrade either your speed or your health. There are anywhere from 3-5 ornaments in a level and 2-4 enemies, and it is randomly generated. However, there is a maximum number of strokes you have to complete each level. 3 strokes for 3 ornaments, 3 strokes for 4 ornaments, and 4 strokes for 5 ornaments. If you use all of your strokes but ornaments are still remaining, you die. You also die if you lose all of your health.

## Files
### `main.py`
The main.py file is the main file for the game. It holds all the main mechanics of the game. Some major functionalities of it are:
* Randomly generating the map, which it does by using the `random` module imported at the top. It also randomly generates the position of the player at the beginning of each level to make the game more random, increasing the strategy required.
* It controls main game functions, such as:
    * Controlling health
    * Controlling amount of ornaments and enemies displayed to the screen using a list
    * Handles upgrades
    * Handles christmas tree levels and amount of coins
    * Makes your score
        * Formula: (max strokes / strokes_used) * 100 * total ornaments in level
        * Maximum score that can be gained is 2500, minimum is 300
    * Handles death, along with functions after death (retrying, going back to main menu, and quitting)
    * Handles player movement
    * Draws everything to the screen each frame
* The `main.py` file also codes the main menu. When you first open the game, it is shown and you can either play the game or quit. It does this by adding and removing a pygame Surface on top of actual gameplay (basically, the main menu is drawm on top of the game)

### `Assets/`
This folder holds all the assets to the game. It holds all the images used, including the character, ornament, enemy, upgrade button, coin icon, christmas tree, and more. It also has the sound effects used in the game, such as the sound for when you hit an enemy, when you collect an ornament, and when you complete the level. It also holds the design of the main menu, which I load onto the screen when I want to display the main menu, but remove when the Play option is selected.

### `coins.txt`
This file is for storing coins. It is a very small file, but it is pretty useful. In the game, if you die and you have coins remaining, the number is written to this file as a string. When you open the game again, it takes the string, converts it to an integer, and uses that as your coins when you first load in.