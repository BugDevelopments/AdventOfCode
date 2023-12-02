import re

def main():
  input_file = 'input2.txt'
  try:
    with open(input_file) as f:
       lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    return

  MAX_RED = 12
  MAX_GREEN = 13
  MAX_BLUE = 14

  def isValidGame(g):
    return (
           all((int(x)<=MAX_RED for x in re.findall(r"(\d+) red",g))) and 
           all((int(x)<=MAX_GREEN for x in re.findall(r"(\d+) green",g))) and
           all((int(x)<=MAX_BLUE for x in re.findall(r"(\d+) blue",g)))
           )
  
  print(sum(i+1 for i in range(len(lines)) if isValidGame(lines[i])))


if __name__ == "__main__":
  main()