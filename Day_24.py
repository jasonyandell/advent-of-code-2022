from collections import defaultdict, deque
from dataclasses import dataclass
from functools import cache
from heapq import heappush
from time import sleep
from aoc import read_lines


sample = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#""".splitlines()

sample_plus1 = """#.######
#.>3.<.#
#<..<<.#
#>2.22.#
#>v..^<#
######.#"""

class Outside:
    blizzards: frozenset[tuple[tuple[int,int],tuple[int,int]]]
    locations: frozenset[tuple[int,int]]
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    start: tuple[int,int]
    goal: tuple[int, int]

    def __init__(self, locations:frozenset[tuple[int,int]], blizzards:frozenset[tuple[tuple[int,int],tuple[int,int]]], min_x, min_y, max_x, max_y, start, goal):
        self.locations = locations
        self.blizzards = blizzards
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.start = start
        self.goal = goal

def parse(lines:list[str]):
    dumb_substr = lambda l,f,t: l[f:t] if f>=0 and t<=len(l) else ""

    blizzards:set[tuple[tuple[int,int],tuple[int,int]]] = set()
    min_x = 10000
    min_y = 10000
    max_x = 0
    max_y = 0
    for y,line in enumerate(lines):
        min_y = min(min_y, y)
        max_y = max(max_y, y)
        for x,ch in enumerate(line):
            if y == 0 and dumb_substr(line,x-1,x+2) == '#.#': start = (x,y)
            if y == max_y and dumb_substr(line, x-1,x+2) == '#.#': goal = (x,y)
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            match ch:
                case '>': blizzards.add(((x,y),(1,0)))
                case '<': blizzards.add(((x,y),(-1,0)))
                case '^': blizzards.add(((x,y),(0,-1)))
                case 'v': blizzards.add(((x,y),(0,1)))
    locations = frozenset((x,y) for (x,y),_ in blizzards)
    hashable_blizzards = frozenset(b for b in blizzards)
    return Outside(locations, hashable_blizzards, min_x+1, min_y+1, max_x-1, max_y-1, start, goal)

@cache  # memoize, this is a huge speedup
def next_blizzard(o:Outside):
    new_blizzards = []
    for (x,y),(dx,dy) in o.blizzards:
        nx = x + dx
        if nx < o.min_x: nx = o.max_x
        if nx > o.max_x: nx = o.min_x

        ny = y + dy
        if ny < o.min_y: ny = o.max_y
        if ny > o.max_y: ny = o.min_y

        new_blizzards.append( (
            (nx, ny), 
            (dx, dy)
        ))
    new_locations = set((x,y) for (x,y),_ in new_blizzards)
    return Outside(frozenset(new_locations), frozenset(new_blizzards), o.min_x, o.min_y, o.max_x, o.max_y, o.start, o.goal)


def out_of_bounds(o:Outside, x, y):
    if (x,y) == o.start: return False
    if (x,y) == o.goal: return False
    if x < o.min_x: return True
    if x > o.max_x: return True
    if y < o.min_y: return True
    if y > o.max_y: return True
    return False

def can_move(o:Outside, x, y):
    if (x,y) == o.start: return True
    if (x,y) == o.goal: return True
    if out_of_bounds(o,x,y): return False
    return (x,y) not in o.locations

def search(init:Outside, animate_queue:list=[]):
    next_blizzard.cache_clear() # important - doesn't seem to hash the entire class

    start_x, start_y = init.start

    visited = set()
    positions = deque([(0,(start_x,start_y,init))])

    t_last = -1
    while positions:
        t,(x,y,curr) = positions.popleft()  

        if t>t_last:
            t_last = t
            animate_queue.append((curr,set((px,py) for _,(px,py,_) in positions) | set((x,y))))

        if (x,y,curr) in visited: continue  
        visited.add((x,y,curr))
        if (x,y) == curr.goal: return (t,curr)

        next = next_blizzard(curr)

        # try staying here + 4 cardinal directions
        attempt = lambda x,y: positions.append((t+1,(x,y,next))) if can_move(next, x, y) else None

        attempt(x,y)
        attempt(x-1,y)
        attempt(x+1,y)
        attempt(x,y-1)
        attempt(x,y+1)
    print("oops")

def outside_to_string(o:Outside,positions):
    assert len(o.locations & positions) == 0
    printed_positions = 0

    things = defaultdict(lambda:[])
    for pos,d in o.blizzards:
        things[pos].append(d)

    lines = []
    for y in range(0,o.max_y+2):
        line = ""
        for x in range(0, o.max_x+2):
            if out_of_bounds(o, x,y): 
                line += '#'
            else:
                here = things[(x,y)]# = [d for (ox,oy),d in o.blizzards if x==ox and y==oy]
                if len(here) == 0: 
                    if (x,y) in positions: 
                        line += '█'
                        printed_positions += 1
                    else: line += '.'
                elif len(here) > 1: line += str(len(here))
                else: 
                    match here[0]:
                        case (1,0): line += '>'
                        case (-1,0): line += '<'
                        case (0,1): line += 'v'
                        case (0,-1): line += '^'
        lines.append(line)

    #assert printed_positions == len(positions)
    return '\n'.join(lines)

def part1(lines:list[str]): return search(parse(lines))[0]

assert 18 == part1(sample)

#print("part 1", part1(read_lines("data/day24.txt")))

def part2(lines:list[str]):
    print("going there")
    animate_queue = []
    init = parse(lines)
    there_time, there_outside = search(init, animate_queue)
    there_outside.goal, there_outside.start = there_outside.start, there_outside.goal
    print("coming back")
    back_time, back_outside = search(there_outside, animate_queue)
    back_outside.goal, back_outside.start = back_outside.start, back_outside.goal
    print("going there again")
    there_again_time, _ = search(back_outside, animate_queue)

    for i in range(90):
        print()
    print('animating')
    boards = []

    for o,p in animate_queue:
        #sleep(.1)
        boards.append(outside_to_string(o,p))


    for board in boards:
        sleep(.05)
        print(board)
        print()

    return there_time + back_time + there_again_time

assert 54 == part2(sample)

print("part 2", part2(read_lines("data/day24.txt")))
