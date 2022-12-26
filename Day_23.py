from collections import defaultdict
from aoc import read_lines

def parse(lines:list[str]):
    elves = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '#': elves.add((x,y))
    return elves

def print_elves(elves):
    for y in range(min(y for _,y in elves), max(y for _,y in elves)+1):
        line = ""
        for x in range(min(x for x,_ in elves), max(x for x,_ in elves)+1):
            line += '#' if (x,y) in elves else '.'
        print(line)
    print()

def run(elves:set[tuple[int,int]], count:int, part2=False):
    add = lambda a,b: (a[0]+b[0],a[1]+b[1])
    check = lambda xr,yr: len(elves & set((x1,y1) for x1 in xr for y1 in yr)) == 0
    north = (lambda x,y: check(range(x-1,x+2), [y-1]), (0,-1))
    dirs = [
        north, # north
        [lambda x,y: check(range(x-1,x+2), [y+1]), (0,1)], # south
        [lambda x,y: check([x-1], range(y-1,y+2)), (-1,0)], # west
        [lambda x,y: check([x+1], range(y-1,y+2)), (1,0)] # east
    ]
    dir = 0

    def no_neighbors(curr):
        (x,y) = curr
        for ax in range(x-1,x+2):
            for ay in range(y-1, y+2):
                neighbor = (ax,ay)
                if neighbor == curr: continue
                if neighbor in elves: return False
        return True


    for c in range(count):
        dests = defaultdict(lambda:set())
        for e in elves:
            if no_neighbors(e): continue

            for d in range(dir, dir+4):
                ok, delta = dirs[d % 4]
                if not ok(*e): continue
                dest = add(e, delta)
                dests[dest].add(e)
                break

        if len(dests) == 0: 
            if part2: return c+1
            break
        
        for dest,es in dests.items():
            if len(es) != 1: continue
            [e] = es
            elves.remove(e)
            elves.add(dest)
        
        #print_elves(elves)

        dir += 1

        # if (c%10 == 0):
        #     print(f"Round {c} moved {len(dests.keys())} elves")

    width = max(x for x,_ in elves)-min(x for x,_ in elves)+1
    height = max(y for _,y in elves)-min(y for _,y in elves)+1
    return width * height - len(elves)


sample = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".splitlines()

simple_sample = """.....
..##.
..#..
.....
..##.
.....""".splitlines()

#print(run(parse(simple_sample), 10))

assert 110 == run(parse(sample), 10)

print("part 1", run(parse(read_lines("data/day23.txt")),10))
print("part 2", run(parse(read_lines("data/day23.txt")),1000000000,True))