import random

from pygorithm.geometry.vector2 import Vector2

MOVEMENT = [Vector2(x=0, y=1), Vector2(x=0, y=-1), Vector2(x=1, y=0), Vector2(x=-1, y=0)]


def random_walk(n):
    """"""
    position = Vector2(x=0, y=0)
    for i in range(n):
        position += random.choice(MOVEMENT)
    return position


number_of_walks = 20000

for walk_length in range(1, 31):
    no_transport = 0
    for i in range(number_of_walks):
        pos = random_walk(walk_length)
        distance = abs(pos.x) + abs(pos.y)
        if distance <= 4:
            no_transport += 1
    no_transport_percentage = float(no_transport) / number_of_walks
    print("Walk size =", walk_length, "/ % of no transport", 100 * no_transport_percentage)
