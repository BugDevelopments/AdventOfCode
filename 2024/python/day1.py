from collections import Counter

def part1(list1, list2):
  total_distance = sum([abs(x-y) for x,y in zip(list1,list2)])
  print("Solution to part 1: ",total_distance)

def part2(list1, list2):
  freq_map = Counter(list2)
  similarity_score = sum(x*freq_map[x] for x in list1)
  print("Solution to part 2:", similarity_score)

def parse_lists(lines):
  list1, list2 = [], []
  for l in lines:
    x,y = map(int, l.split())
    list1.append(x)
    list2.append(y)
  return list1, list2

def read_input_file(input_file):
  try:
      with open(input_file,'r') as f:
        lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error: The input file '{input_file}' was not found.")
    exit(1)
  return lines

def main():
  input_file = "input1.txt"

  lines = read_input_file(input_file)
  list1, list2 = parse_lists(lines)
  list1.sort()
  list2.sort()
  part1(list1, list2)
  part2(list1, list2)

if __name__ == '__main__':
  main()