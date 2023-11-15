<img src='images/logo.png' width='150'>

# Illuminati
This repository contains all the code developed to create the game illuminati

The puzzle implemented refers to the Illuminati, which is played in an areaquadri axadinha, and each house in this area can be of different types. An empty house can be represented by 'o' when it is illuminated, '.' when it is known beforehand that it is impossible to put a lamp and '-' in any other case. A house with a lamp will illuminate the line and column in which it is placed, being represented by '@'. In turn, the locked house indicates an obstacle that prevents the passage of light, being represented by an 'x' when it comes to a simple obstacle. It is denoted that a locked house with a certain number should be surrounded orthogonally by exactly n lamps. In addition, one lamp cannot illuminate another, since a lamp illuminates the line and column in which it is located, until it finds a locked house.

# What can we find in this repository?

Here we can find all the files created to rum the game, such as:

## graphics.py

The library is designed to make it very easy for novice programmers to
experiment with computer graphics in an object oriented fashion. It is
written by John Zelle for use with the book "Python Programming: An
Introduction to Computer Science" (Franklin, Beedle & Associates).

LICENSE: This is open-source software released under the terms of the
GPL (http://www.gnu.org/licenses/gpl.html).

## IlluminatiWindow.py

This file contains the class IlluminatiWindow responsible for creating a window so we can have a graphic representation of the board.

## IlluminatiEngine.py

In this file we find the class IlluminatiEngine, which implements methods (called in the IlluminatiShell) to help change the board where we have the puzzle.

## IlluminatiShell.py

File with the class IlluminatShell. This class implements all the functions that allow us to make plays in the board and save the board state.

In this files were implemented specific functions:

### do_mr
Command that shows the existing puzzle in a file.

### do_cr
Command that takes a name file as his parameter and loads it to the memory.

### do_gr
Command that allows us to save the board in his current state. Takes the name file of the board used as his parameter.

### do_grh
Command that allows to save all the alterations made to a board step by step.

### do_jr
Command that allows the player to select the place where the lamp is placed or from where it is removed. It uses as his parameters 2 numbers that indicate the row and column where we want to put or remove the lamp.

### do_mi
Command that illuminates the board when it finds a lamp. The board is the parameter of this function.

### do_est1
Command that implements a strategy to solve the puzzle. This allows to automatically place lamps in the neighbor houses of a locked house, if the number of available houses is equal to the number of the locked house. The board is the parameter of this function.

### do_est2
Command that implements a strategy to solve the puzzle. This allows the player to automatically illuminate the row and column where the lamp was placed until it finds the limit of the board or a locked house. The board is the parameter of this function.

### do_est3
Command that implements a strategy to solve the puzzle. This enables the possibility of making impossible plays by marking the spaces that would lead to them. The board is the parameter of this function.

### do_est4
Command that implements a strategy to solve the puzzle. This function not only enables the placement of lamps in the two houses shared in the diagonal of specific combinations (if the locked houses are 0 and 2, or 1 and 3), but also places necessarily two lamps in a diagonal of a specific pair of locked houses, like 2 and 3.  The board is the parameter of this function.

### do_est5
Command that implements a strategy to solve the puzzle. This allows us to place a lamp where the house can be illuminated if there is a lamp on it. The board is the parameter of this function.

### do_undo
Command that undoes the previous command.

### do_resolve
Command that automatically solves the puzzle. The board is the parameter of this function.

### do_ver
Command that let's us visualize the current state of the puzzle.


## Authors: 

- Alexandra Coelho (PG45458)
- Andreia Gomes (PG45463)
- Catarina Ferreira (PG45467)
- Daniela Lemos (PG45469)

### do_sair
Command that allows us to quit the program.

### cmdloop
Creats a menu to access all the previous functions using keywords.
