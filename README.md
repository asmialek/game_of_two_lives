# Game of Two Lives
Immigration (a variation of Conway's Game of Life) arena simulator.

## Launch
Python of versrion at least `3.6` is required. Run `pip install -r requirements.txt`. Execute `game_of_two_lives.pyw`.

## Rules
In this variant of Game of Life the rules are as given:
* There are three states: Blue, Red and Dead.
* Any live cell with fewer than and two more than three live neighbors dies.
* Any live cell with two or three live neighbors lives on to the next generation.
* Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
* The color of the alive cell is determined by the color of majority of it's neighbours. If there is no vantage, the cell retains it's color.
* The grid has torroidal geometry, where the grid wraps from top to bottom and left to right.

As this is a Game of Life gamification attempt, in the last turn, the cells of each color shall be counted and the one with higher count is considered a winner.

More can be found:
*https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules*

## Game modes
While currently there is no option to change grid and seed sizes, if the development is continues couple of game modes will be added, consisting of various grid sizes, duration, numbers of seeds and their dimensions. The current and only one is defined by:
 * Number of seeds: 2
 * Turns: 32
 * Grid size: 16 x 16 
 * Seed size: 4 x 4
 
## Seed preparaion
To prepare a seed for a game, create a `.txt` file with four rows of four characters. Dot character, that is  `.`, is considered a dead cell. Any other is considered alive. 

The seeds can be chosen form game interface, but the files must be written have exactly to the specification.
