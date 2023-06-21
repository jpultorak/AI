# Artificial Inteligence
## *2023 University of Wroclaw course*
### P1 (Randomized and search algorithms) 
- **z1.py**  solution to cooperative rook & king mate [(CodinGame)](https://www.codingame.com/training/medium/cooperative-mate-with-rook)
- **z2.py**  given set of words and text without spaces, add spaces (maximizing length)
- **z3.py**  simulation to determine poker probabilities
- **z4.py, z5.py** - (simplified) Nonogram solver (WalkSat inspired)
### P2 (A* algorithm, reduction of uncertainty)
- **komandos.py**  solution to commando puzzle using random/heuristic moves in order to reduce uncertainty, and BFS with node pruning
- **komandos2.py**  solution to commando puzzle using A* search, with admissible/non-admissible heuristic
- **nonograms.py**  general Nonogram solver (WalkSat inspired)
- **sokoban.py** solution to sokoban puzzle
### P3 (Constraint satisfaction problems, backtracking)
- **nonograms.py**  Nonogram solver using CSP and backtracking
- **sudoku.py**  python program, which given sudoku puzzle, generates code for SWI-PROLOG, which solves the problem 
- **storms.py** python program, which given storms puzzle, generates code for SWI-PROLOG, which solves the problem 
### P4 (Othello, Chess agents)
- #### **Othello** 
    Current agent uses minimax with alpha-beta pruning. Evaluation function is a linear combination of disks balance, mobility, frontier size, and corners captured with different weights for early, mid and late game. I tested two ways of representing othello state: **agents/reversi_state.py** with 8x8 matrix as board, and  **agents/reversi_bitboard.py** with two bitarrays for white/black disks. [Flood fill](https://www.chessprogramming.org/Dumb7Fill)-like algorithm with bitshifts is used for move generation/resolution and computing evaluation function. Agent was tested in 1v1 matchups against other agents (**reversi/bosses**) using `python3 local_ai_dueller_2023.py [--verbose 0|1|2] [--num_games N] reversi PROGRAM0.sh PROGRAM1.sh`. Possible improvements: Transposition tables, openings books, better evaluation (e.g. neural networks to determine optimal weights of each function components).
    
- #### **Chess** 
    Agent uses alpha beta search with quiescence search, with MVV-LVA heuristic for move ordering. Position evaluation consists of material balance, PST, mobility and king safety, all depending on stage of the game. For early stages agent has got opening book implemented. 


### P5 (Chess agents tournament)
- Each agent has pieces values and mobility as its parameters. Population of 80 agents was randomly selected, and tournament was performed. Agents used quinesence search with depth 2. Results turned out to be consistent with common chess pieces valuation i.e queen > rook > bishop > knight.

