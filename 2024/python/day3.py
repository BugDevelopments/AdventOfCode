import re

def read_input_file(input_file):
  try:
      with open(input_file,'r') as f:
        string = f.read()
  except FileNotFoundError:
    print(f"Error: The input file '{input_file}' was not found.")
    exit(1)
  return string

def part1(string):
  mul_operands = re.findall(r'mul\((\d+),(\d+)\)',string)
  res = sum(int(x)*int(y) for x,y in mul_operands)
  print("Solution to part 1: ",res)

def part2(string):
  N = r"don't\(\)"
  Y = r"do\(\)"
  M = r"mul\((\d+),(\d+)\)"
  pattern=f"{N}|{Y}|{M}"

  res = 0
  dont = False
  for match in re.finditer(pattern,string):
    token = match.group(0)
    if token == "don't()":
      dont = True
    elif token == "do()":
      dont = False
    elif not dont:
      res += int(match.group(1))*int(match.group(2))

  print("Solution to part 2: ",res)

def main():
  input_file = "input3.txt"
  string = read_input_file(input_file)
  part1(string)
  part2(string)

if __name__ == '__main__':
  main()