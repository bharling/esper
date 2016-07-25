import esper
import random
import time
import multiprocessing


#################################
# Define some generic components:
#################################
# class Velocity:
#     def __init__(self, x=0.0, y=0.0):
#         self._x = multiprocessing.Value('f', x)
#         self._y = multiprocessing.Value('f', y)
#
#     @property
#     def x(self):
#         return self._x.value
#
#     @x.setter
#     def x(self, value):
#         self._x.value = value
#
#     @property
#     def y(self):
#         return self._y.value
#
#     @y.setter
#     def y(self, value):
#         self._y.value = value


class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self._x = multiprocessing.Value('f', x)
        self._y = multiprocessing.Value('f', y)

    @property
    def x(self):
        return self._x.value

    @x.setter
    def x(self, value):
        self._x.value = value

    @property
    def y(self):
        return self._y.value

    @y.setter
    def y(self, value):
        self._y.value = value


# class Velocity:
#     def __init__(self, x=0.0, y=0.0):
#         self.x = x
#         self.y = y


class Position:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


##########################
#  Define some Processors:
##########################
class ReportProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, vel in self.world.get_component(Velocity):
            returned_vel = vel
            print("Returned values:", returned_vel.x, returned_vel.y)


class GravityProcessor(esper.ParallelProcessor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("Processing", self.name)
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            vel.y += 1


class RelayProcessor(esper.ParallelProcessor):
    def __init__(self):
        super().__init__()

    def process(self):
        print("Processing", self.name)
        for ent, vel in self.world.get_component(Velocity):
            vel.x += 1


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

    report_proc = ReportProcessor()
    gravity_proc = GravityProcessor()
    relay_proc = RelayProcessor()
    world.add_processor(report_proc)
    world.add_processor(gravity_proc)
    world.add_processor(relay_proc)

    # Give the processes time to spawn:
    time.sleep(1)

    for i in range(100):
        world.process()
        time.sleep(0.01)
        # if i == 50:
        #     world.remove_component(entity=1, component_type=Position)
        #     world.remove_component(entity=2, component_type=Position)
        #     world.remove_component(entity=3, component_type=Position)
        #     world.remove_component(entity=4, component_type=Position)
        #     world.remove_component(entity=5, component_type=Position)
