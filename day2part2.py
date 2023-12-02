import re

def main():
  input_file = 'input2.txt'
  try:
    with open(input_file) as f:
       lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    return

  max_red = lambda g: max(map(int,re.findall(r"(\d+) red",g)))
  max_blue = lambda g: max(map(int,re.findall(r"(\d+) blue",g)))
  max_green = lambda g: max(map(int,re.findall(r"(\d+) green",g)))
  
  print(sum(max_red(g)*max_blue(g)*max_green(g) for g in lines))


if __name__ == "__main__":
  main()