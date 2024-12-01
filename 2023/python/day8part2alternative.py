import math
import re
from sympy.ntheory.modular import solve_congruence

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)


def computeProfile(instructions, graph,start_node):
  class State:
    def __init__(self, start):
      self.node = start
      self.steps = 0
      self.path = []
      self.completed = False
      self.pathLength = 0
      self.visit()

    def visit(self):
      if (self.node,self.steps % len(instructions)) in self.path:
        self.completed = True
        self.periodIndex = self.path.index((self.node,self.steps % len(instructions))) # path[pathLength] == path[periodIndex] 
        self.pathLength = self.steps 
        return True      
      self.path.append((self.node,self.steps % len(instructions)))
      return False
      
    def next(self):
      self.node = graph[self.node][0 if instructions[self.steps % len(instructions)]=='L' else 1]
      self.steps += 1
      return self.visit()
      
    def getProfile(self):
      # all indices of Z-states on the path
      Z = { e for e,node in enumerate(self.path) if node[0][2]=='Z'}
      # offsets of Z-states that lie on the period
      C = { e-self.periodIndex for e in Z if e>=self.periodIndex}
      return (self.periodIndex, self.pathLength-self.periodIndex, Z, C) 
              # p0                  #c0                #Z   #C
  s = State(start_node)
  while not s.completed:
    s.next()
  return s.getProfile()


INPUT_FILE = "input8.txt"

lines = readInputFile(INPUT_FILE)
instructions = lines[0]
graph = { x[0] : (x[1],x[2]) for l in lines[2:] for  x in [re.findall(r"[A-Z]{3}",l)] } 

start_nodes = [ x for x in graph if x[2] == 'A' ]
profiles = [ computeProfile(instructions,graph,start_node) for start_node in start_nodes]


# first check if a common Z-state is reached already before the 
# n = p0 + c0*k , 
 # n == r (mod c0) , x>=n 
#  n == c+p0 (mod c0), for c in C
moduli = [ P[1] for P in profiles]
remainders = [ P[3] for P in profiles]
from itertools import product

for R in product(*remainders):
  R=[x+y for x,y in zip(R,[P[0] for P in profiles])]
  print(*(zip(R,moduli)))
  print(solve_congruence(*(zip(R,moduli))))