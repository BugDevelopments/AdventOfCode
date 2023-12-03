import re

def main():
  # open input file and save its lines
  input_file = 'input3.txt'
  try:
    with open(input_file) as f:
        lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    return
  
  # checks if the number in lines[row][start:end] is adjacent to a symbol
  def ispartnumber(row,start,end):
    issymbol = lambda c: (c !='.' and not c.isdigit())
    N = [ (slice(max(0,row-1),row), slice(max(0,start-1),end+1)), 
          (slice(row,row+1),slice(max(0,start-1),start)), 
          (slice(row,row+1),slice(end,end+1)),
          (slice(row+1,row+2),slice(max(0,start-1),end+1)) ]

    return any( issymbol(c) for (R,C) in N for l in lines[R] for c in l[C])

  # compute sum of all part numbers
  sum = 0
  for i in range(len(lines)):
    for m in re.finditer(r"(\d+)",lines[i]):
      if ispartnumber(i,m.start(), m.end()): # __dddd_
        sum += int(m.group())

  print(sum)    

if __name__ == '__main__':
  main()