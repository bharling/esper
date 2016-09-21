from concurrent.futures import ProcessPoolExecutor


##################################
#  Templates
##################################
class Processor:
    def __init__(self):
        self.components = None

    def process(self, *args):
        raise NotImplementedError


class Velocity:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class MoveProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.components = Velocity, Position

    def process(self, payload):
        ent, vel, pos = payload
        pos.x += vel.x
        pos.y += vel.y
        return payload


##################################
#  Test code:
##################################

move_processor = MoveProcessor()
vel = Velocity(34, 5)
pos = Position(20, 20)

package = (1, vel, pos)


procs = []
with ProcessPoolExecutor() as executor:
    future = executor.submit(move_processor.process, package)
    ent, vel, pos = future.result()
    print(pos.x, pos.y)
