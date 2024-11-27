from argparse import ArgumentParser

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
    def __init__(self, size, numbers):
        self.size = size
        self.numbers = numbers

    def neighbors(self, pos):
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


    def positions(self):
        for x in range(self.size.x):
            for y in range(self.size.y):
                yield Vector2(x, y)

    
    def from_input(filename):
        with open(filename) as file:
            board_size = Vector2.zero()
            numbers = {}

            board_size.x, board_size.y = next(file).split()

            for line in file:
                posx, posy, number = line.split()
                numbers[Vector2(posx, posy)] = int(number)

        return Board(board_size, numbers)


def encode_Npi(position, number, positive=True):
    vals = [str(position.x), str(position.y), str(number)]

    # Make sure that the code number never starts with 0
    code = "1"

    for val in vals:
        code += str(val).rjust(3, "0")

    if not positive:
        code = "-" + code

    return code


def main(args):
    board = Board.from_input(args.input)

    for pos, num in board.numbers.items():
        print(encode_Npi(pos, num))

    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", default="input.in", type=str, help="The instance file.")

    main(parser.parse_args())