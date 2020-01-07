# KakuroSolver

Kakuro is a logic puzzle that is often referred to as a mathematical transliteration of the crossword. 
We try to solve it as a CSP with multiple AI algorithms. 
Our goal is to show how different CSP algorithms behave during the solution of Kakuro.

The algorithms we use are:
- BackTracking (BT)
- Forward Checking (FC)
- Maintaining Arc Consistency (MAC)

Those algorithms were forked by [AIMA code](https://github.com/aimacode/aima-python)

## Getting Started
Make sure you have a python release higher than 3.3

### Downloading
Download source code by typing:

``` git clone https://github.com/nikosgalanis/KakuroSolver.git ```

## Examples

In the directory examples, there are plenty of kakuro puzzles, with dificulties and sizes that vary.

## Running

You can run each of the examples by:
``` python3 src/kakuro.py examples/<DesiredPuzzle> ```

## Comparing the Algorithms

When executed, the program provides the solution for the puzzle, as well as the time and itterations taken by each algorithm, thus making them easy to compare

This project was implemented for the needs of the course "Artificial Inteligence"
