from functools import cache
from itertools import chain
import re
from time import sleep
from aoc import read_lines

sample = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32""".splitlines()

def eq(x): return x
def add(x,y): return x+y
def sub(x,y): return x-y
def mul(x,y): return x*y
def div(x,y): return x/y
def match(x,y): return x - y

def parse(lines:list[str], part2=False):
    tree = {}
    for line in lines:
        [name,rhs] = re.match("(.*): (.*)", line).groups()
        if rhs.isnumeric():
            tree[name] = (eq,int(rhs))
        else:
            [left,op,right] = re.match("(.*) (.) (.*)", rhs).groups()
            args = (left, right)
            if part2:
                if name == "root": 
                    tree[name] = (match, args)
                    continue
            match op:
                case '+': tree[name] = (add, args)
                case '-': tree[name] = (sub, args)
                case '*': tree[name] = (mul, args)
                case '/': tree[name] = (div, args)
    return tree


def evaluate(tree, name):
    @cache
    def inner(name):
        op, args = tree[name]
        if (op == eq): return args
        else: 
            lhs = inner(args[0])
            rhs = inner(args[1])
            value = op(lhs, rhs)            
            return value

    return inner(name)

assert 152 == evaluate(parse(sample), "root")

print("part 1", evaluate(parse(read_lines("data/day21.txt")), "root"))


def part2(lines:list[str]):
    tree = parse(lines, True)

    def at(i):
        tree["humn"] = (eq,i)
        return evaluate(tree, "root")
    
    def derivative_at(i): return at(i+1)-at(i)

    x = 0
    while at(x) != 0:
        # straightup newton's method
        x = x - at(x) / derivative_at(x)
    return int(x)

assert 301 == part2(sample)
print("part 2", part2(read_lines("data/day21.txt")))