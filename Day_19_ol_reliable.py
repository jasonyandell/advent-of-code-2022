

# collect x
# try each
# - if can_build -> build robot
# - don't build robot

import copy
from dataclasses import dataclass
from functools import cache
from aoc import read_lines


@dataclass(frozen=True)
class Blueprint:
    ore:int
    clay:int
    obsidian_ore:int
    obsidian_clay:int
    geode_ore:int
    geode_obsidian:int

@dataclass(frozen=True)
class Rocks:
    ore:int
    clay:int
    obsidian:int
    geode:int

def parse(lines:list[str]) -> dict[int,Blueprint]:
    blueprints = {}
    for i,line in enumerate(lines):
        [ore,clay,obsidian_ore,obsidian_clay,geode_ore,geode_obsidian] = \
            [int(s) for s in line.split() if s.isdigit()]
        #print(ore,clay,obsidian_ore,obsidian_clay,geode_ore,geode_obsidian)
        blueprints[i+1] = Blueprint(ore,clay,obsidian_ore,obsidian_clay,geode_ore,geode_obsidian)
    return blueprints


sample = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".splitlines()


def collect_ore(delta:Rocks): return Rocks(delta.ore+1,delta.clay,delta.obsidian,delta.geode)
def collect_clay(delta:Rocks): return Rocks(delta.ore, delta.clay+1,delta.obsidian,delta.geode)
def collect_obsidian(delta:Rocks): return Rocks(delta.ore, delta.clay,delta.obsidian+1,delta.geode)
def collect_geode(delta:Rocks): return Rocks(delta.ore, delta.clay,delta.obsidian,delta.geode+1)

def buy_ore(blueprint:Blueprint, rocks:Rocks): return Rocks(rocks.ore - blueprint.ore, rocks.clay,rocks.obsidian,rocks.geode)
def buy_clay(blueprint:Blueprint, rocks:Rocks): return Rocks(rocks.ore - blueprint.clay, rocks.clay,rocks.obsidian,rocks.geode)
def buy_obsidian(blueprint:Blueprint, rocks:Rocks): return Rocks(rocks.ore - blueprint.obsidian_ore, rocks.clay - blueprint.obsidian_clay,rocks.obsidian,rocks.geode)
def buy_geode(blueprint:Blueprint, rocks:Rocks): return Rocks(rocks.ore - blueprint.geode_ore, rocks.clay, rocks.obsidian - blueprint.geode_obsidian,rocks.geode)

def add(a:Rocks, b:Rocks): return Rocks(a.ore+b.ore, a.clay+b.clay,a.obsidian+b.obsidian,a.geode+b.geode)

@dataclass(frozen=True)
class State:
    rocks:Rocks
    delta:Rocks

def make_state(blueprint, rocks, delta, spend, update) -> State:
    new_rocks = spend(blueprint, rocks)
    if new_rocks.clay >= 0 and new_rocks.geode >= 0 and new_rocks.ore >= 0 and new_rocks.obsidian >= 0:
        if new_rocks.clay < 60 and new_rocks.ore < 60 and new_rocks.obsidian < 60: # don't collect too much rocks
            new_delta = update(delta)
            return State(add(new_rocks, delta), new_delta)
    return State(add(rocks, delta), delta)

@cache
def get_next_states(blueprint:Blueprint, rocks:Rocks, delta:Rocks):
    next_state_list = [
        make_state(blueprint, rocks, delta, buy_geode, collect_geode),
        make_state(blueprint, rocks, delta, buy_obsidian, collect_obsidian),
        State(add(rocks, delta), delta),
        make_state(blueprint, rocks, delta, buy_clay, collect_clay),
        make_state(blueprint, rocks, delta, buy_ore, collect_ore),
    ]
    next_states = set(next_state_list)
    return next_states


found_geode_time = {}
def run_blueprint(blueprint:Blueprint, rocks:Rocks, delta, time: int, time_limit:int):
    global found_geode_time

    if time > time_limit: 
        return rocks
       
    if delta.geode < found_geode_time[time]: 
        return Rocks(0,0,0,0)

    if delta.geode > found_geode_time[time]:
        for t in range(time, time_limit+1):
            found_geode_time[t] = max(found_geode_time[t], delta.geode)
        print(found_geode_time)


    next_states = get_next_states(blueprint, rocks, delta)
    
    results = []
    for state in next_states:
        r = run_blueprint(blueprint,state.rocks,state.delta,time+1,time_limit) 
        results.append(r)

    best = max(results, key=lambda x:x.geode)

    #print(found_geode_time)
    return best
        
#blueprints = parse(sample)
blueprints = parse(read_lines("data/day19.txt"))

# score = 0
# for i in sorted(blueprints.keys()):
#     get_next_states.cache_clear()
#     found_geode_time = {}
#     for t in range(1,25): found_geode_time[t] = 0
#     print(f"Blueprint {i}")
#     r = run_blueprint(blueprints[i], Rocks(0,0,0,0),Rocks(1,0,0,0),1,24)
#     score += i * r.geode
#     print(i, r)
# print("score", score)

score = 1
for i in sorted(blueprints.keys()):
    if i > 3: continue
    get_next_states.cache_clear()
    found_geode_time = {}
    for t in range(1,33): found_geode_time[t] = 0
    print(f"Blueprint {i}")
    r = run_blueprint(blueprints[i], Rocks(0,0,0,0),Rocks(1,0,0,0),1,32)
    score += i * r.geode
    print(i, r)
print("score", score)
