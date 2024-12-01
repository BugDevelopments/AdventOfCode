import math
import re

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

# counts the steps required to reach the node 'ZZZ' from 'AAA' by following
# the instructions through the graph
def countSteps(instructions, graph):
  step_count = 0
  node = 'AAA'
  N = len(instructions)
  while node != 'ZZZ':
    node = graph[node][0 if instructions[step_count % N]=='L' else 1]
    step_count += 1
  return step_count


INPUT_FILE = "input8.txt"
lines = readInputFile(INPUT_FILE)
instructions = lines[0]
graph = { x[0] : (x[1],x[2]) for l in lines[2:] for  x in [re.findall(r"[A-Z]{3}",l)] } 
print(countSteps(instructions, graph))