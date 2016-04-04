#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
import pickle
import sys
import time
import timeit

import esper


##########################
# Simple timing decorator:
##########################
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        result_times.append((time2 - time1)*1000.0)
        return ret
    return wrap


##############################
#  Instantiate the game world:
##############################
world = esper.CachedWorld() if '--use-cache' in sys.argv[1:] else esper.World()


#################################
# Define some generic components:
#################################
class Velocity:
    def __init__(self):
        self.x = 0
        self.y = 0


class Position:
    def __init__(self):
        self.x = 0
        self.y = 0


class Health:
    def __init__(self):
        self.hp = 100


class Command:
    def __init__(self):
        self.attack = False
        self.defend = True


class Projectile:
    def __init__(self):
        self.size = 10
        self.lifespan = 100


class Damageable:
    def __init__(self):
        self.defense = 45


class Brain:
    def __init__(self):
        self.smarts = 9000


#############################
# Set up some dummy entities:
#############################
def create_entities(number):
    for _ in range(number // 2):
        enemy = world.create_entity()
        world.add_component(enemy, Position())
        world.add_component(enemy, Velocity())
        world.add_component(enemy, Health())
        world.add_component(enemy, Command())

        thing = world.create_entity()
        world.add_component(thing, Position())
        world.add_component(thing, Health())
        world.add_component(thing, Damageable())


#############################
# Some timed query functions:
#############################
@timing
def single_comp_query():
    for _, _ in world.get_component(Position):
        pass


@timing
def two_comp_query():
    for _, (_, _) in world.get_components(Position, Velocity):
        pass


@timing
def three_comp_query():
    for _, (_, _, _) in world.get_components(Position, Damageable, Health):
        pass


#################################################
# Perform several queries, and print the results:
#################################################
results = {1: {}, 2: {}, 3: {}}
result_times = []

for amount in range(1000, 5000, 100):
    create_entities(amount)
    for _ in range(20):
        single_comp_query()

    result_min = min(result_times)
    print("Query one component, {} Entities: {:f} ms".format(amount, result_min))
    results[1][amount] = result_min
    result_times = []
    world.clear_database()
    gc.collect()

for amount in range(1000, 5000, 100):
    create_entities(amount)
    for _ in range(20):
        two_comp_query()

    result_min = min(result_times)
    print("Query two components, {} Entities: {:f} ms".format(amount, result_min))
    results[2][amount] = result_min
    result_times = []
    world.clear_database()
    gc.collect()

for amount in range(1000, 5000, 100):
    create_entities(amount)
    for _ in range(20):
        three_comp_query()

    result_min = min(result_times)
    print("Query three components, {} Entities: {:f} ms".format(amount, result_min))
    results[3][amount] = result_min
    result_times = []
    world.clear_database()
    gc.collect()


########################################
# Save the results to disk for plotting:
########################################
if len(sys.argv) > 1:
    if sys.argv[1] == "--save":
        file_name = time.strftime('results-%Y%m%dT%H%M%S.pickle')
        print("\nSaving benchmark results to '{}'...".format(file_name))
        print("Display these results by running  plot-results.py {}".format(file_name))
        with open(file_name, 'wb') as picklefile:
            pickle.dump(results, picklefile)
    else:
        print("You can save these results to disk with the --save argument.")
