import random
from game.GameLogic.Food import Plant, Meat
from game.Camera import random_pos_outside_camera

def spawn_food_outside_view(game, food_type=None):
    x, y = random_pos_outside_camera(game)

    if food_type is not None:
        food = food_type(x, y)
    else:
        if random.random() < 0.5:
            food = Plant(x, y)
        else:
            food = Meat(x, y)

    game.food_group.add(food)
