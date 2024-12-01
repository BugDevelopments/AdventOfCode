import numpy as np
import math

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

# Solution idea:
# Let t be the time, d be the distance and c the charging time,
# then the the distance travelled by the boat will be: p(t,d,c) = (t-c)*c
# A charging time 0<=c<=t is a winner iff p(t,d,c)>=d
# This is equivalent to a quadratic inequality in c
# p(t,d,c) >= d   iff
# (t-c)*c >= d    iff
# c^2-tc+d <= 0   
#
# If c0 and c1 are the roots of the quadratic equation c^2-tc+d , then
# (c-c0)(c-c1) = c^2-tc+d <=0 
# 
# There are 3 possible cases:
# 1. c0 and c1 are complex but not real numbers => no solutions if d !=0 , and (t+1) solutions if d=0 (any c between and t is a solution in this case)
# 2. c0 and c1 are both real numbers with
# 2.1 c0 = c1 => no solutions if c0 isn't an integer, and 1 solution (c0=c1 itself) if c0 is an integer
# 2.2 c0 != c1 => any c between min(c0,c1) and max(c0,c1) is a solution => max(c0,c1)-min(c0,c1)+1 solutions
#
# numSolutions(t,d) returns the the number of integer solutions c with 0<=c<=t of the inequality c^2-tc+d<=0
def numSolutions(t,d):
    c0, c1 = np.roots([1,-t,d])
    if isinstance(c0,complex): 
      return 0 if d !=0 else t+1
    c0, c1 = min(c0,c1), max(c0,c1)
    if c1==c0:
      if math.floor(c0)==c0: # if c0 is an integer
        return 1
      else:
        return 0
    return min(math.floor(c1),t)-max(math.ceil(c0),0)+1

def main():
  # open input file and save as list of line
  input_file = 'input6.txt'
  lines = readInputFile(input_file)
  lines = [l.split(':')[1].split() for l in lines]
  # lines[0] = list of times
  # lines[1] = list of distances

  t = int(''.join(lines[0]))
  d = int(''.join(lines[1]))  
  res=numSolutions(t,d)
  print(res)

if __name__ == '__main__':
  main()