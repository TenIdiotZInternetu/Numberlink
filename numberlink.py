from argparse import ArgumentParser
from itertools import combinations
import subprocess

GLUCOSE_PATH = "./glucose/simp/glucose"

class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def up():
        return Vector2(0, 1)
    
    def down():
        return Vector2(0, -1)
    
    def left():
        return Vector2(-1, 0)
    
    def right():
        return Vector2(1, 0)
    
    def zero():
        return Vector2(0, 0)
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return "<{}, {}>".format(self.x, self.y)


class Board:
    def __init__(self, size: Vector2, numbers: dict[Vector2, int]):
        self.size = size
        self.numbers = numbers

    def neighbors(self, pos:Vector2) -> list[Vector2]:
        neighbors = []

        # Assure that pos is in bounds of the board
        assert 0 <= pos.x < self.size.x and 0 <= pos.y < self.size.y

        # Don't return neighbors outside of the board
        if pos.x > 0:
            neighbors.append(pos + Vector2.left())
        if pos.x < self.size.x - 1:
            neighbors.append(pos + Vector2.right())
        if pos.y > 0:
            neighbors.append(pos + Vector2.down())
        if pos.y < self.size.y - 1:
            neighbors.append(pos + Vector2.up())

        return neighbors


    def tiles(self):
        for x in range(self.size.x):
            for y in range(self.size.y):
                yield Vector2(x, y)


    def highest_number(self) -> int:
        return max(self.numbers.values())
    

    def numbered_tiles(self):
        return iter(self.numbers.keys())

    
    def from_input(filename: str):
        with open(filename) as file:
            sizex, sizey = next(file).split()
            board_size = Vector2(int(sizex), int(sizey))

            numbers = {}
            for line in file:
                posx, posy, number = line.split()
                numbers[Vector2(int(posx), int(posy))] = int(number)

        return Board(board_size, numbers)


def encode_Npi(position: Vector2, number: int, positive=True) -> str:
    vals = [str(position.x), str(position.y), str(number)]

    # Make sure that the code number never starts with 0
    code = "1"

    for val in vals:
        code += str(val).rjust(3, "0")

    if not positive:
        code = "-" + code

    return code


def encode_cnf(board: Board) -> frozenset[frozenset[str]]:
    number_count = board.highest_number()
    clauses = set()

    empty_tiles = set(board.tiles()) - set(board.numbered_tiles())

    # Initial tiles with numbers
    for pos, num in board.numbers:
        clauses.add(encode_Npi(pos, num))

    # Only one number per tile
    for pos in board.tiles():
        for i in range(number_count):
            for j in range(number_count):
                if i == j: continue
                clauses.add(encode_onlyOneNum(pos, i, j))
                
    # Exactly one neighbor on numbered tiles
    for pos in board.numbered_tiles():
        for i in range(number_count):
            clauses |= encode_neighborCount(board, 1, pos, i)

    # Exactly two neighbors on empty tiles
    for pos in empty_tiles:
        for i in range(number_count):
            clauses |= encode_neighborCount(board, 2, pos, i)

    return frozenset(clauses)


def encode_onlyOneNum(pos: Vector2, i: int, j: int) -> frozenset[str]:
    clause = set()
    clause.add(encode_Npi(pos, i, False))
    clause.add(encode_Npi(pos, j, False))

    return frozenset(clause)


def encode_neighborCount(board: Board, count: int, pos: int, num: int) -> frozenset[str]:
    assert 0 <= count <= 4

    clauses = set()
    neighbors = board.neighbors(pos)
    n = len(neighbors)

    for k in range(n + 1):
        if k == count: continue

        for i_comb in combinations(range(n), k):
            clause = set()

            for i, nebr in enumerate(neighbors):
                clause.add(encode_Npi(nebr, num, i not in i_comb))

            clauses.add(frozenset(clause))

    return frozenset(clauses)


def cnf_to_file(cnf: frozenset[frozenset[str]], var_count:int, file_name: str):
    with open(file_name, "w") as file:
        file.write(f'p cnf {0} {1}'.format(str(var_count), str(len(cnf))))

        for clause in cnf:
            file.write(" ".join(clause))


def run_glucose(cnf_file, verbosity):
    return subprocess.run([GLUCOSE_PATH, '-model', '-verb=' + str(verbosity) , cnf_file], stdout=subprocess.PIPE)


def main(args):
    board = Board.from_input(args.input)
    cnf = encode_cnf(board)
    
    var_count = board.size.x * board.size.y * board.highest_number()
    cnf_file = cnf_to_file(cnf, var_count, args.output)
    result = run_glucose(cnf_file, args.verbosity)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", default="input.in", type=str, help="The instance file.")
    parser.add_argument("-o", "--output", default="output.cnf", type=str, help="The file to write CNF into")
    parser.add_argument("-v", "--verbosity", default=1, type=int, choices=range(0,2), help="Verbosity of the SAT solver used.")

    main(parser.parse_args())