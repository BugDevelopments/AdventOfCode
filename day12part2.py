def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

# Thanks to 0xrdf for this solution: https://www.youtube.com/watch?v=0kvDfjjJPog 
# Using the @cache decorator on a recursive method to compute the number of solutions  
from functools import cache

@cache
def get_combinations(s,L): 
  if len(s) < sum(L)+len(L)-1:
    return 0

  # base cases
  if len(s)==0:
    if sum(L)==0:
      return 1
    else:
      return 0
  
  if len(L)==0:
    if '#' in s:
      return 0
    else:
      return 1
  #

  # there are two cases for recursion, for the 2 different interpretations of an `?`     
  total = 0
  # add number of combinations after we consume a '.' or set '?' to '.'
  if s[0] in ".?":
    total += get_combinations(s[1:],L)
  
  # add number of combinations after we consume '#'*L[0]+'.' and L[0] (setting all ? on the way to #)
  n = L[0]
  if '.' not in s[0:n] and (len(s)==n or s[n] in '.?'):
    total += get_combinations(s[n+1:],L[1:])
  
  return total

INPUT_FILE = 'input12.txt'

lines = readInputFile(INPUT_FILE)
lines = [l.split() for l in lines]
lines = [(x,list(map(int,y.split(','))) )for x,y in lines]

print(sum(get_combinations('?'.join([s]*5),tuple(nums*5)) for s,nums in lines))