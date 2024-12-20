from itertools import product
from operator import add, mul
from functools import reduce
import re

def read_input_file(input_file):
  try:
    with open(input_file,'r') as f:
      lines = [re.findall(r'(\d+)',l) for l in f] # simply get all nunbers in the line
      lines = [[int(x) for x in l] for l in lines]
      return lines # each element of lines is now a vector of numbers [res, op1, op2, op3, ... , opk] , where res is the desired result and op1 ,..., opk the k operands
  except FileNotFoundError:
    print(f"Error: The input file '{input_file}' was not found.")
    exit(1)

# gets a number x and a pair z=(op,y) of an operator op and a number y as input and returns op(x,y)
# Example: ev(4,add,10) == add(4,10) == 14
#          ev(4,mul,10) == mul(4,10) == 40
# this function is then used with functools.reduce 
ev = lambda x, z: z[0](x, z[1])

# checks if any combination of operators applied to the list of operands yields the result
# we can get an iterable of any combination of operators with itertools.product(operators, repeat=n) , which would generate
# all combinations of operators of length n
check = lambda result, operands, operators: any(
    result == reduce(ev, zip(operators, operands[1:]), operands[0])
    for operators in product(operators, repeat=len(operands) - 1)
)

def part1(lines):    
  res = sum(
      result
      for result, *operands in lines
      if check(result, operands,[add,mul])
  )
  print("Solution to part 1:", res)

# define the concatenation operator on ints
cat = lambda x,y: int(str(x)+str(y))   

def part2(lines):
  res = sum(
      result
      for result, *operands in lines
      if check(result, operands,[cat,add,mul])
  )
  print("Solution to part 2:", res)

def main():
  input_file = "input7.txt"
  lines = read_input_file(input_file)
  part1(lines)
  part2(lines)

if __name__ == "__main__":
  main()