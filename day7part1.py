def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)


def handtype(h):
   # make a histogram of the letters occuring in h
   d = dict.fromkeys(h,0)
   for c in h:
      d[c] += 1

   hist = sorted(d.values())

   # 5 of a kind
   if hist == [5]:
      return '7'
   # 4 of a kind
   if hist == [1,4]: 
      return '6'
   # full house
   if hist == [2,3]:
      return '5'
   # 3 of a kind
   if hist == [1,1,3]:
      return '4' 
   # 2 pairs
   if hist== [1,2,2]:
      return '3'
   # 1 pair 
   if hist== [1,1,1,2]:
      return '2'
   # high card
   return '1'

# It holds for any two hands h1, h2 that h1 is ranked higher than h2 iff handrank(h1) < handrank(h2) 
def handrank(h):
   v=h.translate(str.maketrans("TJQKA","ABCDE")) # makes hands lexicographically comparable 
   return handtype(h)+v 

def main():
  input_file = 'input7.txt'
  lines = readInputFile(input_file)
  lines = [l.split() for l in lines]
  lines.sort(key=lambda x: handrank(x[0]))
  print(sum((e+1)*int(h[1]) for e,h in enumerate(lines)))

if __name__ == '__main__':
   main()
