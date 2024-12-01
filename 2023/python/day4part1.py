def main():
  # open input file and save its lines
  input_file = 'input4.txt'
  try:
    with open(input_file) as f:
       lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    return

  cards = [[c.split() for c in l.split(':')[1].split('|')] for l in lines]
  res = sum(int(2**((sum((x in c[0]) for x in c[1])-1))) for c in cards)  
  print(res)
  
if __name__ == "__main__":
  main()