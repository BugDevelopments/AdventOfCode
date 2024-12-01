from itertools import combinations

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

def replace(s,T):
  s = list(s)
  for i in T:
    s[i]='.'

  return ''.join(s)

# Brute force: Try all ways to replace ?'s by '.' and '#'
# The number of ?s to be replaced by # must be the sum of numbers in the list minus number of #s already in s  
def solve():
  profile = lambda s: [len(w) for w in s.split('.') if w] # example: profile('#??#...#..##..?##..')=[4,1,2,3]

  total = 0
  for s,nums in lines:
    count = 0
    P = [i for i in range(len(s)) if s[i]=='?'] # list of positions of '?'
    k = len(P)-(sum(nums)-s.count('#')) # snumber of '.''s that need to be assigned to '?'s
    for T in combinations(P,k): # Iterating over all k-subsets of P
      if profile(replace(s,T)) == nums:
        count += 1
    total += count
  print(total)

INPUT_FILE = 'input12.txt'

lines = readInputFile(INPUT_FILE)
lines = [l.split() for l in lines]
lines = [(x,list(map(int,y.split(','))) )for x,y in lines]

solve()