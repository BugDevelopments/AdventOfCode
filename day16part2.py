def deflect(c,d,loc):
  x,y = d
  i,j = loc
  if c=='|': 
    return [((i+x,j+0),(x,0))] if x else [((i+y,j),(y,0)),((i-y,j),(-y,0))]
  if c=='-':
    return [((i,j+y),(0,y))] if y else [((i,j+x),(0,x)),((i,j-x),(0,-x))]
  if c=='/':
    (0,1)
    return [((i-y,j-x),(-y,-x))]
  if c=='\\':
    return [((i+y,j+x),(y,x))]
  return [((i+x,j+y),(x,y))]
      
def traverse(M,start_loc=(0,0),start_dir=(0,1)):
  inM = lambda x,y: 0<=x<len(M) and 0<=y<len(M[x])
  visited = set()
  stack = [(start_loc,start_dir)]
  while stack:
    (i,j),(x,y) = stack.pop()
    if ((i,j),(x,y)) not in visited and inM(i,j):
      visited.add(((i,j),(x,y)))
      stack.extend(deflect(M[i][j],(x,y),(i,j)))
  return visited

def getMaxEnergy(M):
  return max(
    max(len(set(map(lambda x:x[0],traverse(M,start_loc=(i,0),start_dir=(0,1))))) for i in range(len(M))),
    max(len(set(map(lambda x:x[0],traverse(M,start_loc=(0,j),start_dir=(1,0))))) for j in range(len(M[0]))),
    max(len(set(map(lambda x:x[0],traverse(M,start_loc=(i,len(M[i])-1),start_dir=(0,-1))))) for i in range(len(M))),
    max(len(set(map(lambda x:x[0],traverse(M,start_loc=(len(M)-1,j),start_dir=(-1,0))))) for j in range(len(M[-1])))
  )  

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

INPUT_FILE = 'input16.txt'
lines = readInputFile(INPUT_FILE)
print(getMaxEnergy(lines))