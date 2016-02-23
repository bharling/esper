import esper
import random
import time
import multiprocessing


#################################
# Define some generic components:
#################################
class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


##########################
#  Define some Processors:
##########################
class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            vel.y += 1
            print("Local", vel.y)


class GravityProcessor(esper.ParallelProcessor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, vel in self.world.get_component(Velocity):
            vel.y += 1
            print("Multicore", vel.y)


###############
#  Helper utils
###############
def create_entities(world, number):
    for _ in range(number):
        enemy = world.create_entity()
        world.add_component(enemy, Position(x=random.randint(0, 500), y=random.randint(0, 500)))
        world.add_component(enemy, Velocity())


if __name__ == "__main__":
    world = esper.ParallelWorld()
    create_entities(world, 5)

    movement_proc = MovementProcessor()
    gravity_proc = GravityProcessor()

    world.add_processor(movement_proc)
    world.add_processor(gravity_proc)

    for _ in range(5):
        world.process()

    manager = multiprocessing.Manager()

    shared_dict = manager.dict()
    shared_dict["key"] = manager.list()

    shared_dict["key"].append(1)
    print(shared_dict["key"])

    shared_dict["key"][0] += 1
    print(shared_dict["key"])

    shared_dict["key2"] = manager.dict()

    shared_dict["key2"]["internal_dict"] = 1
    print(shared_dict["key2"])

    shared_dict["key2"]["internal_dict"] += 1
    print(shared_dict["key2"])

    time.sleep(5)