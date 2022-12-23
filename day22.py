import re
from time import sleep
from aoc import read_lines_raw

sample="""        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".splitlines()

def parse(lines:list[str]):
    [blank_line] = [i for i,line in enumerate(lines) if len(line)==0]
    grid = [line + ' '*(len(lines[0])-len(line)) for line in lines[:blank_line]]
    direction_string = lines[blank_line+1]

    steps:list = []
    ch = ""
    for s in direction_string:
        if s.isdigit(): ch += s
        else: 
            if len(ch): steps.append(int(ch))
            steps += s
            ch = ""
    if len(ch): steps.append(int(ch))
    return grid, steps

def first(input:list[str]):
    s = "".join(input)
    matches = re.match(" *([#\.])", s)
    (first_non_space,) = matches.groups()
    index = s.index(first_non_space)
    return index

def assign(grid:list[str], pos:tuple[int,int], value:str):
    x,y = pos
    line = list(grid[y])
    line[x] = value
    grid[y] = "".join(line)

def walk(grid:list[str], steps:list):
    debug_grid = list(map(str,grid))

    width = len(grid[0])

    def move(curr,dir):
        nonlocal grid
        cx,cy=curr
        dx,dy=dir

        x,y = cx+dx, cy+dy

        col = [line[cx] for line in grid]
        if dy < 0:
            if y < 0 or grid[y][x] == ' ': y = len(grid)-1 - first(col[::-1])
        if dy > 0:
            if cy+dy >= len(grid) or grid[y][x] == ' ': y = first(col)

        row = [ch for ch in grid[cy]]
        if dx < 0:
            if cx+dx < 0 or grid[y][x] == ' ': x = width-1 - first(row[::-1])
        if dx > 0:
            if cx+dx >= width or grid[y][x] == ' ': x = first(row)

        if grid[y][x] == '.': return (x,y)
        else: return curr

    curr = (grid[0].index('.'), 0)
    directions = [(1,0), (0,1), (-1,0), (0,-1)]
    debug_directions = ['>','v','<','^']
    direction = 0
    assign(debug_grid, curr, debug_directions[direction])

    while len(steps):
        sleep(.1)

        step = steps[0]

        match steps[0]:
            case 0: 
                steps.pop(0)
            case int(): 
                curr = move(curr, directions[direction])
                steps[0] -= 1
            case 'L': 
                direction = (direction - 1) % len(directions)
                steps.pop(0)
            case 'R': 
                direction = (direction + 1) % len(directions)
                steps.pop(0)

        print(f"{curr=} {step=}, dir={debug_directions[direction]}")
        assign(debug_grid, curr, debug_directions[direction])
        print('\n'.join(debug_grid))
        print()

    return 1000*(curr[1]+1) + 4 * (curr[0]+1) + direction
        

print(walk(*parse(sample)))
#print(walk(*parse(read_lines_raw("data/day22.txt"))))
