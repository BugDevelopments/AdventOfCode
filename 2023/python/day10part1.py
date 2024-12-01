def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

def findS(maze):
  for i in range(len(maze)):
    for j in range(len(maze[i])):
      if maze[i][j] == 'S':
        return (i,j)
  
charToTile = {
  '|': {'N','S'},
  '-': {'W','E'},
  'L': {'N','E'},
  'J': {'N','W'},
  '7': {'S','W'},
  'F': {'S','E'},
  'S': {},
  '.' : {}
}

INPUT_FILE = "input10.txt"
maze = readInputFile(INPUT_FILE)

mazeTile = lambda T: charToTile[maze[T[0]][T[1]]]
inMaze = lambda x,y: 0<=x<=len(maze) and 0<=y<=len(maze[x])
goTo = lambda x,y,d:  {'W':(x,y-1), 'N':(x-1,y), 'E':(x,y+1), 'S':(x+1,y)}[d]
inv = lambda x: {'S':'N', 'N':'S', 'W':'E', 'E':'W'}[x]
directionsFrom = lambda x,y: [ d for d in ('N','E','S','W') for z in {goTo(x,y,d)} if inMaze(*z) and (inv(d) in mazeTile(z))]
# find start node coordinates
S = findS(maze)  
charToTile['S'] = directionsFrom(*S)

def getLoop():
  d = directionsFrom(*S)[0]
  loop = {S}
  next_node = goTo(*S,d)
  while next_node != S:
    cur_node = next_node
    loop.add(cur_node)
    d = (mazeTile(cur_node)-{inv(d)}).pop()
    next_node = goTo(*cur_node,d)  
  return loop

loop = getLoop()
print(len(loop)//2)