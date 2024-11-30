# Numberlink
CNF encoding of the [Numberlink puzzle](https://en.wikipedia.org/wiki/Numberlink) for a Propositional Logic assignment. This application attempts to solve both variants where each tile on the grid either must or might not be filled.

## Input
On the first line of the input there are 2 numbers:

`{grid_width} {grid_height}`

Then $2n$ lines follow, where n is the count of numbers present on the grid. On each of the n lines there are 3 numbers:

`{x} {y} {i}`

where *i* is the number filled in the (x, y) coordinates of the grid. Upper left tile has coordinates (0, 0)


## Encoding
The puzzle can be simplified from drawing lines between lines to filling numbers into empty spaces. We can write $i$ into a tile where there would  normally be a line connecting 2 tiles with the number $i$. That's we introduce only one variable.

$N(p, i)$ where $i$ is the number being written into the tile at coordinates $p$

In the CNF file, the $N(p, i)$ is encoded as a 7 digit number, where the 1st digit is always 1, so the number has fixed length, the 2nd and 3rd digits are x coordinate of $p$, the 4th and 5th digits are the y coordinate of $p$, and 6th and 7th digits are $i$.


## Constraints

### 1. Initial numbering
$\bigwedge_{p, i \in input} N(p, i)$

### 2. Not more than one number per tile
$\bigwedge_{p} \bigwedge_{i \ne j} \neg N(p, i) \vee \neg N(p, j)$

### 3. Initially numbered tiles can only have one neighbor tile with the same number
Same as being connected to one other tile.

$\bigwedge_{x \in X} \bigwedge_{i} N(x, i) \implies \Big( N(\larr, i) \wedge \neg N(\uarr, i) \wedge \neg N(\rarr, i) \wedge \neg N(\darr, i)\Big) \vee \Big(\neg N(\larr, i) \wedge N(\uarr, i) \wedge \neg N(\rarr, i) \wedge \neg N(\darr, i)\Big) \vee ...$  

where $X$ is set of the initially numbered tiles. Arrow symbols represent a neighbor tile leftward, above, rightward and below of $x$. At the right side of the implication is a DNF, where each conjuction contains one literal for each of the neighbors. Exactly one literal is always positive, others are negative.

We can get rid of the implication:

$\bigwedge_{x \in X} \bigwedge_{i} \neg N(x, i) \vee \Big( N(\larr, i) \wedge \neg N(\uarr, i) \wedge \neg N(\rarr, i) \wedge \neg N(\darr, i)\Big) \vee \Big(\neg N(\larr, i) \wedge N(\uarr, i) \wedge \neg N(\rarr, i) \wedge \neg N(\darr, i)\Big) \vee ...$ 

getting us another DNF. We can get CNF by finding a complement to the set of all models for the theory with this DNF as its single axiom. 

### 4. Initially empty tiles have exactly two neighbor tiles with the same number
Same as the previous constraint but we take tiles from the set empty tiles, and in conjunction there are 2 positive and 2 negative literals.

### 5. Each tilie has at least one number written into it
If we are solving that variant of the puzzle

$\bigwedge_{p} \bigvee_{i} N(p, i)$

## Command line options
