from itertools import product
from sympy.ntheory.modular import solve_congruence
from math import ceil
import re


# Idea:
# Every path must at some point lead into a cycle (because there are only finitely many nodes, so at some step a node must reoccur on the path)
# There can be several z-nodes (=nodes ending with 'Z') on the cycle and on the path to the cycle.
# We track each path from each a-node (=nodes ending with 'A') following the instructions simultaneously and record 
# the positions of the z-nodes we encounter. 
# Either all paths simultaneously reach a z-node before they have all completed a cycle or at some point they all have completed a cycle.
# Once they all have completed a cycle, we can then compute the minimal number of steps needed  for them to all reach synchronosuly a z-state on their cycles by
# solving a system of modular congruence equations (using sympy). There are multiple solutions to the congruence system. The smallest solution is the one
# we need.

# In each step of the synchronous path traversal we will reach a new 'State', which is a data structure to collect information
# about the nodes that have already been traversed 
class State:

  instructions = [] # this will hold the direction instructions that is given in the input as a list of 0's and 1's where 0 stands for 'L' and 1 stands for 'R'
  M = len(instructions) 
  graph = dict() # a dictionary that is holding the graph that is given in the input in such a way that graph[node][0] / graph[node][1] are the left/right-successors of node
  a_nodes = [] # the list of nodes that end with the letter 'A' which are the starting nodes for the paths to be traversed
  z_nodes = [] # the list of nodes that end with the letter 'Z' which are the ending nodes for the paths to be traversed
  
  # Given a node of the form 'XYZ' , where X,Y,Z are any three letters constructs a new State
  def __init__(self,node):
    self.node = (node,0)  # A state s with s.node =(n,i) has the 3-letter name `n`, and the continues into the direction `instruction[i]``
    self.complete = False # Whether we have already completed a cycle or not
    self.cycle_length = None 
    self.path_length = None
    self.steps = 0 # Number of steps already taken on this path
    self.visited_nodes = [] # A list of the nodes traversed so far in the order they have been traversed
    self.visited_znodes = set() # A set of the z-nodes that have been traversed so far

    self._visit() 

  def takeStep(self):
    self.node = (State.graph[self.node[0]][State.instructions[self.steps % self.M]], (self.steps+1) % self.M)
    self.steps += 1

    self._visit()    

  def _visit(self):
    if self.node in self.visited_nodes: # has this node already been traversed before? Then we have completed a cycle
      idx = self.visited_nodes.index(self.node) # get the step idx at which the node was traversed before, then
      if not self.complete:                     # visited_nodes[0:idx] is the path leading to the cycle and visted_nodes[idx:steps] is the cycle
        self.complete = True
        self.path_length = self.steps 
        self.cycle_length = self.path_length-idx
    else:                               # otherwise node hasn't been traversed before
      self.visited_nodes.append(self.node)
      if self.isZNode():                # is it a z-node?
        self.visited_znodes.add(self.steps)
        print(f'appended ZNode: {self.node=} with {self.steps=}')     

  def isZNode(self):  
    return self.node[0] in State.z_nodes
  
  def isANode(self):
    return self.node[0] in State.a_nodes

  def init(instructions, graph):
      State.instructions = instructions
      State.M = len(instructions) 
      State.graph = graph

  # computes and returns the smallest number n so that the paths that start at the nodes in `start_nodes` all end in a node from `end_node` after n steps`    
  def solveSimultaneously(start_nodes, end_nodes):
    State.a_nodes = start_nodes
    State.z_nodes = end_nodes

    states = [ State(n) for n in State.a_nodes]

    # traverse the paths until either all are in a z-state or all have completed a cycle
    while not all(s.complete for s in states):
      if all(s.isZNode() for s in states):
        return states[0].steps
      
      for s in states:
        s.takeStep()
    
    # from here on every path has completed a cycle but they haven't simultaneously reached a z-state yet
    
    # We first solve a system of congruence equations that is defined as follows:
    # For each path we have computed the following numbers
    # p (=s.cycle_length): cycle-length 
    # n (=s.path_length) : path-length      
    # # r (in s.visited_znodes) : number of steps on the cycle to reach a z-state (there can be several z-states on the same cycle, leading to one r for each such z-state)
    # Then we reach the z-state always after n+k*p+r steps for any k>=0 that is always after a number of steps x with x mod p = r and x>=n
    #
    # For each path s we have numbers (p_s,n_s,r_s) and so reach a z-state after x steps with x mod p_s = r_s and x>=n_s
    # So we have to find a number x that simultaneously fulfills the equations x mod p_s = r_s and x>=n_s for all s 
    # This can be done with the function solve_congruence from the sympy library
    moduli = [s.cycle_length for s in states]
    remaindersets = [s.visited_znodes for s in states]
    
    max_pathlength = max(s.path_length for s in states)
    solutions = []
    for rem in product(*remaindersets): # for all possible combinations of z-states on the loops we calculate a solution 
      solution = solve_congruence(*zip(rem,moduli))
      print(f"congruence solutions of {rem=}: {solution=}")
      if solution:
        # possibly adjust the solution. Choose the smallest k so that
        # solution[0]+solution[1]*k >=max_pathlength <=>
        k = ceil((max_pathlength-solution[0])/solution[1])
        solutions.append(solution[0]+k*solution[1])
    # the smallest solution is the solution
    return min(solutions)

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

def main():
  # input parsing
  INPUT_FILE="input8.txt"
  lines = readInputFile(INPUT_FILE)
  instructions = list(map(int,lines[0].replace('L','0').replace('R','1')))
  graph = { x[0] : (x[1],x[2]) for l in lines[2:] for  x in [re.findall(r"[A-Z]{3}",l)] } 
  start_nodes = [ x for x in graph if x[2] == 'A' ]
  end_nodes = [ x for x in graph if x[2] == 'Z']

  State.init(instructions,graph)
  print(State.solveSimultaneously(start_nodes, end_nodes))     

if __name__ == '__main__':
  main()