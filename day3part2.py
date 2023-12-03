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
  
  # create a dictionary mapping coordinates (i,j) to the number that intersects that coordinate in a digit  
  loc = {}
  for i in range(len(lines)):
    for m in re.finditer(r"(\d+)",lines[i]):
      for j in range(m.start(),m.end()):
        loc[(i,j)]=m
  
  def getnums(i,j): 
    # neighbour points of (i,j)
    N = [(i-1,j-1), (i-1,j), (i-1,j+1), (i,j-1), (i,j+1), (i+1,j-1), (i+1,j), (i+1,j+1)]
    # return set of numbers in the neighbourhood of (i,j) 
    return { loc.get(x,None) for x in N }-{None}
     
  
  # compute sum of of gear ratios (=product of neighbouring two numbers) 
  sum = 0
  for i in range(len(lines)):
    for j in range(len(lines[i])):
      if lines[i][j] != '.' and not lines[i][j].isdigit():
        nums = getnums(i,j)
        if len(nums)==2:
          x,y = nums
          sum += int(x.group())*int(y.group())
  print(sum)


if __name__ == "__main__":
  main()