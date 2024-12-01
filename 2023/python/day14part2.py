def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

def getLoad(M):
  return sum(sum((c=='O')*(len(M)-i) for i,c in enumerate(col)) for col in zip(*M))
      
def turnCW(M):
  return [l[::-1] for l in (map(list, zip(*M)))]

def tiltNorth(M):
  if type(M[0])!='list':
    M = [list(l) for l in M]
  for j in range(len(M[0])):
    free = 0 # invariant: assert( all(c[j]=='.' for c in M[free:i]) )
    for i in range(len(M)):
      if M[i][j] == 'O':
        if free != i:
          M[free][j] = 'O'
          M[i][j] = '.'
        free += 1
      elif M[i][j] == '#':
        free = i+1
  return M

def cycle(M):
  for _ in range(4):
    M = tiltNorth(M)
    M = turnCW(M) 
  return M

INPUT_FILE = 'input14.txt'
lines = readInputFile(INPUT_FILE)
H=[tiltNorth(lines)]
next = cycle(H[-1])
while next not in H:
  H.append(next)
  next = cycle(next)
c = H.index(next)
print(getLoad(H[(1000000000-c) % (len(H)-c)+c]))