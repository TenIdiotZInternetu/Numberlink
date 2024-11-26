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
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)


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