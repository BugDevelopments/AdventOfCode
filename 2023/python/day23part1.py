INPUT_FILE = "input23.txt"

with open(INPUT_FILE) as f:
  maze = [l.strip() for l in f]

def find_longest_path(vx,vy,wx,wy,maze):
  M = len(maze) # rows
  N = len(maze[0]) # columns

  isValid = lambda vx,vy: 0<=vx<M and 0<=vy<N 
  isForest = lambda vx,vy: maze[vx][vy] == '#'
  isPath = lambda vx,vy: maze[vx][vy] == '.'
  isSlope = lambda vx, vy: maze[vx][vy] in "^v><"
  slopes = { '>':(0,1), '<':(0,-1), '^':(-1,0), 'v':(1,0)}
  dirs = { (-1,0), (1,0), (0,-1), (0,1) }

  def getNeighbours(vx, vy):
    if isForest(vx,vy):
      return []
    if isSlope(vx,vy):
      dx,dy = slopes[maze[vx][vy]]
      return [(vx+dx, vy+dy)] if isValid(vx+dx,vy+dy) else []
    if isPath(vx,vy):
      return sorted([(vx+dx, vy+dy) for dx, dy in dirs if isValid(vx+dx,vy+dy) and not isForest(vx+dx, vy+dy)])
  
  path = [(vx,vy,iter(getNeighbours(vx,vy)))]
  max_length = 1
  visited = { (vx,vy) }
  # Do a depth-first search through the maze
  while path:
    vx,vy,it = path[-1]
    try:
      if (vx,vy)==(wx,wy): # destination reached
        if len(path) > max_length: # found longer path
          max_length = len(path)
        raise "GOTO except:" 
      
      nx,ny = next( (nx,ny) for nx,ny in it if (nx,ny) not in visited ) # get first unvisited neighbour, raises exception if iteration it is finished

      path.append((nx,ny,iter(getNeighbours(nx,ny))))
      visited.add((nx,ny))
      
    except: # no more unvisited neighbours (or destination reached)
      path.pop() # remove node from path
      visited.discard((vx,vy))
  return max_length-1 # -1 because we count only the steps taken, not the number of nodes on the path

print(find_longest_path(0,1,len(maze)-1,len(maze[-1])-2,maze))