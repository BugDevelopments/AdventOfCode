import re

def main():
  input_file = 'input2.txt'
  try:
    with open(input_file) as f:
       lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    return
  
  max_color = lambda c,g: max(map(int,re.findall(fr"(\d+) {c}",g))) # returns the maximal number of c-colored balls in game g
  print(sum(max_color('red',g)*max_color('blue',g)*max_color('green',g) for g in lines))


if __name__ == "__main__":
  main()