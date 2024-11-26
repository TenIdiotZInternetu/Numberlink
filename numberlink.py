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