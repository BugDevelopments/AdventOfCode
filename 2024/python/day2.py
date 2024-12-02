def read_input_file(input_file):
  try:
      with open(input_file,'r') as f:
        lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error: The input file '{input_file}' was not found.")
    exit(1)
  return lines

def parse_input(lines):
  reports = [[int(x) for x in l.split()] for l in lines]
  return reports

def part1(reports):
  num=0
  for r in reports:
    if all(1<=y-x<=3 for x,y in zip(r,r[1:])) or all(1<=x-y<=3 for x,y in zip(r,r[1:])):
        num += 1 
  print("Solution to part 1:",num)

def part2(reports):

  def is_increasing(diff):
    not_inc = [i for i,d in enumerate(diff) if not 1<=d<=3] # set of indexes of steps that are not increasing

    match not_inc:
      case []: # every step is increasing
        return True
      case [i] if i==len(diff)-1 or i==0: # the first or the last step are not increasing
        return True
      case [i]: # some step in the middle is not increasing
        return 1<=diff[i]+diff[i+1]<=3 or 1<=diff[i-1]+diff[i]<=3
      case [i,j] if i-1==j or i+1==j: # two successive steps are not increasing
        return 1<=diff[i]+diff[j]<=3
      case _: # any other case
        return False
  
  def is_decreasing(diff):
      return is_increasing([-d for d in diff])

  num=0
  for r in reports:
    diff = [y-x for x,y in zip(r, r[1:])]
    if is_increasing(diff) or is_decreasing(diff):
      num += 1

  print("Solution to part 2:",num)

def main():
  input_file = "input2.txt"
  lines = read_input_file(input_file)
  reports = parse_input(lines)
  part1(reports)
  part2(reports)

if __name__ == '__main__':
  main()