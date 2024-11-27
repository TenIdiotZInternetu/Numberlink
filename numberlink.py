from argparse import ArgumentParser
from itertools import combinations

class Vector2:
    def __init__(self, x, y):
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
        assert pos.x >= 0 and pos.y >= 0 and pos.x < self.size.x and pos.y < self.size.y

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
            board_size = Vector2.zero()
            numbers = {}

            board_size.x, board_size.y = next(file).split()

            for line in file:
                posx, posy, number = line.split()
                numbers[Vector2(posx, posy)] = int(number)

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


def encode_cnf(board: Board) -> set[set[str]]:
    number_count = board.highest_number()
    clauses = set()

    empty_tiles = set(board.tiles()) - set(board.numbered_tiles())

    for pos in board.tiles():
        for i in range(number_count):
            for j in range(number_count):
                clauses.add(encode_onlyOneNum(pos, i, j))
                
    for pos in board.numbered_tiles():
        for i in range(number_count):
            clauses.add(encode_oneSameNeighbor(board, pos, i))

    for pos in empty_tiles:
        for i in range(number_count):
            clauses.add(encode_twoSameNeighbors(board, pos, i))

    return clauses


def encode_onlyOneNum(pos: Vector2, i: int, j: int):
    return set(
        encode_Npi(pos, i, False),
        encode_Npi(pos, j, False)
    )


def encode_oneSameNeighbor(board: Board, pos: int, num: int) -> set(str):
    clause = set()
    neighbors = board.neighbors(pos)
    n = len(neighbors)

    for k in range(n):
        if k == 3: continue

        for i_comb in combinations(range(n), k):
            for i, nebr in enumerate(neighbors):
                if i in i_comb:
                    clause.add(encode_Npi(nebr, num, True))
                else:
                    clause.add(encode_Npi(nebr, num, False))

    return clause


def main(args):
    board = Board.from_input(args.input)

    for pos, num in board.numbers.items():
        print(encode_Npi(pos, num))

    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", default="input.in", type=str, help="The instance file.")

    main(parser.parse_args())