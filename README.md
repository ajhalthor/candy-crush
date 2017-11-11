# Candy Crush 

Its almost halloween, the scariest day of the year _Boo_! As a kid, all that was on my mind were _jack o'lanterns_, mama's pumpkin pie and of course, _trick-or-treating_! I've always had a penchant for sugarry treats, and halloween was the only time I could get high on sugar. My cousins and I had to share our merch, but that wouldn't happen without a fight. What is best way you can get the most candy? We are going to solve this problem today with an **Adversarial Search** technique called $\alpha \beta$ pruning.  


## Rules

Our modification of candy crush is a two player game in which each player tries to maximize his/her share of candy from a box. The box is divided into cells and each cell is either empty or filled with a piece candy of a specific type.

At the beginning of each game, all cells are filled with candy. Players play in turn and can pick a cell of the box in their own turn and claim all candies of the same type, in all cells that are connected to the selected cell through horizontal and vertical paths. For each selection or move, the agent is rewarded a numeric value which is the square of the number of fruits claimed in that move. Once an agent picks the candy from the cells, their empty place will be filled with other candies on top of them (which fall down. Work with it), if any. In this game, no candy is added during game play. Hence, players play until all candies have been claimed.

Another game constraint is that each kid (player) has only limited time to pick the best candy. Otherwise, the other will cut him off. Each kid has 300 seconds for _all_ moves. He can split it in any way he wishes. The overall score of each player is the sum of rewards gained for every turn. The game will terminate when there is no candies left in the box or when a player has run out of time.

## Game Setup with Example

Consider a 10 x 10 game board with 4 types of candies denoted by digits 0, 1, 2 and 3 in the cells. By analyzing the game, a player should decide which location to pick next. Let’s assume that it has decided to pick the cell highlighted in red and yellow in figure 1.

![alt text](mics/instruction_fig.png "Logo Title Text 1")

Figure 2 shows the result of executing this action: all the horizontally and vertically connected candies of the same type (here, the selected candy is of type 0) have been replaced by a * symbol (which represents an empty cell). The player will claim 14 candies of type 0 because of this move and thus will be rewarded $14^2 = 196 $ points.

Figure 3 shows the state of the game after the empty space is filled with candies falling from cells above. That is, for each cell with a \* in figure 2, if candies are present above, they will fall down. When a candy that was on the top row falls down, its previous location is marked as empty (i.e., it becomes a * symbol). That is, no new candies are injected to the top of the board. In addition to returning the column and row of your selected fruit, the player will also need to return this resulting state after gravity has been applied. The game is over when all cells are empty, and the winner is determined by the total number of points, that is, $\textit{sum of [candies taken on each move]}^2$ (it is possible to end in a draw if both players score the same).

In figure 3, the opponent player then decided to pick the location highlighted in green and yellow. Upon selecting this cell, all 12 candies of type 1 connected to that cell will be given to the opponent player and thus the opponent player will gain $12^2 = 144$ points. In figure 4, cells connected to the selected cell are marked with * and in figure 5 you see how some of those picked candies are replaced with the contents of cells above (candies above fell down due to gravity).

## Input File Structure

The file input.txt in the current directory of your program will be formatted as follows:

- **First line**: Second line: Third line: Next n lines:
- **Second Line**: integer n, the width and height of the square board (0 < n <= 26)
- **Thrid Line**: integer p, the number of fruit types (0 < p <= 9)
- **Next N Lines**: strictly positive floating point number, your remaining time in seconds the N x N board, with one board row per input file line, and N characters (plus end-of-line marker) on each line. Each character can be either a digit from 0 to p-1, or a * to denote an empty cell.

## Output File Structure

The file output.txt which your program creates in the current directory should be formatted as follows:
- **First line**: your selected move, represented as two characters:
    - A letter from A to Z representing the column number (where A is the leftmost column, B is the next one to the right, etc), and
    - A number from 1 to 26 representing the row number (where 1 is the top row, 2 is the row below it, etc).


- **Next N Lines**: The n x n board just after your move and after gravity has been applied to make any fruits fall into holes created by your move taking away some fruits (like in figure 3).

## My Implementation

This repository includes a **python3.6** version of the game just described. 


1\. Read the input file and store:

    - N: the dimensions of Board
    - p: number of candies
    - t: amount of time left to complete _all_ moves
    - The board itself

2\. Determine the amount of time required to complete a move based on total time and number of moves that can be made this board. I came up with the following formula: $$ \textit{time_per_move} = \frac{t}{\textit{num_moves}} $$   This notion makes sense as longer games would involve less time per move.

3\. We perform **Iterative Deepening** $\bf{\alpha \beta}$ **Pruning**, starting with $ \textit{max_depth} = 2$. This will determine the optimal move, looking head 2 boards. 


4\. Once the optimal move is obtained, we increase the maximum depth $ \textit{max_depth} = 3$. The move will be even better than the move chosen before as we look ahead **3 moves**. Repeat this process either until all possible paths have been searched or time for the move runs out. In the latter case, return the _latest_ optimal move found. 

## Examples

Consider the sample input:

```
4
2
234.56
1101
0101
1001
0001
```

My program makes the following move:

```
C1
***1
1**1
01*1
11*1
```

In other words, it picked the candy in the 1st row and 3rd column _0_. This is clearly the best move. Lets consider a less obvious input:

```
5
3
100
*****
11111
22222
11111
22222
```

My program makes the following move:

```
A2
*****
*****
22222
11111
22222
```

So it took the row of 1s at the top. This is in fact the best case scenario. Had the next row of 2s been taken, then the opponent would have a chance to get 10 _1s_. The same is the case for the 4th row consisting of _1s_. The opponent would have the opportunity to get 10 _2s_ on the next board. Our agent is quite cautious.

However, there are some cases in which the best move isn't so obvious. Consider the sample Input:

```
10
4
300
3102322310
0121232013
3021111113
0221031132
0230011012
0323321010
2003022012
2202200021
0130000020
2200022231
```

A possible output for this file is:

```
H5
31******10
010*****13
3022322*13
0221232*32
0221111*12
0331031310
2020011012
2203321121
0103022120
2232222231
```

This is in fact the best move (5, 8). You may argue that we should have taken the _1_ and we would have 15 candies instead of the 14 now. Had we done that, then the opponent would have also been able to get 15 candies in his next move. In my case, the apponent can only get a maximum of 12. 



