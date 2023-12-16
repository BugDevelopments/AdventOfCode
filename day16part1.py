def deflect(c,d,loc):
  x,y = d
  i,j = loc
  if c=='|': 
    return [((i+x,j+0),(x,0))] if x else [((i+y,j),(y,0)),((i-y,j),(-y,0))]
  if c=='-':
    return [((i,j+y),(0,y))] if y else [((i,j+x),(0,x)),((i,j-x),(0,-x))]
  if c=='/':
    return [((i-y,j-x),(-y,-x))]
  if c=='\\':
    return [((i+y,j+x),(y,x))]
  return [((i+x,j+y),(x,y))]
      
def traverse(M):
  inM = lambda x,y: 0<=x<len(M) and 0<=y<len(M[x])
  visited = set()
  stack = [((0,0),(0,1))]
  while stack:
    (i,j),(x,y) = stack.pop()
    if ((i,j),(x,y)) not in visited and inM(i,j):
      visited.add(((i,j),(x,y)))
      stack.extend(deflect(M[i][j],(x,y),(i,j)))
  return visited

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

INPUT_FILE = 'input16.txt'
lines = readInputFile(INPUT_FILE)
visited = set(map(lambda x:x[0],traverse(lines)))
print(len(visited))