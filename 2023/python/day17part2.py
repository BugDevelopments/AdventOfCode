from heapq import heappush, heappop
from itertools import product
from math import inf

# Using the Dijkstra algorithm to find the shortest path 
def findShortestDistance(G):
  m,n = len(G),len(G[0])

  norm = lambda x: 0 if x==0 else x//abs(x)
  dirs = {(0,1),(0,-1),(1,0),(-1,0)}
  directions = {(i*x,i*y) for i in range(4,11) for x,y in dirs}
  # distance matrix that is operated on by the Dijkstra algorithm
  dist = { (x,y,i,j): inf for i,j in product(range(m),range(n)) for x,y in directions } 

  isValid = lambda x,y,i,j: 0<=i<m and 0<=j<n and (x,y) in directions

  # return the set of direct neighbours of a node (x,y,i,j)
  def nb(x,y,i,j):
    if i==j==0:
      N = { (0,4,0,4) , (4,0,4,0) }
    else:
      dx,dy = norm(x),norm(y)
      N = { (x+dx,y+dy,i+dx,j+dy)}
      N |= {(4*dy,4*dx,i+4*dy,j+4*dx)}
      N|= {(-4*dy,-4*dx,i-4*dy,j-4*dx)}
    return { T for T in N if isValid(*T)}

  # return the energy incured when walking from node (i,j) to node (a,b)
  def cost(i,j,a,b):
    if j<b:
      return sum(G[a][x] for x in range(j+1,b+1) )
    if b<j:
      return sum(G[a][x] for x in range(b,j))
    if i<a:
      return sum(G[x][b] for x in range(i+1,a+1))
    if a<i:
      return sum(G[x][b] for x in range(a,i))
    return 0

  pq = [] # priority queue
  heappush(pq,(0,0,0,0,0)) # push the start node on the heap

  while pq:
    d,x,y,i,j = heappop(pq)
    if (i,j)==(m-1,n-1): # destination node (bottom-right corner) reached?
      print(d)
      break
    for (u,v,a,b) in nb(x,y,i,j): 
      c = d+cost(i,j,a,b)
      if c<dist[(u,v,a,b)]:
        dist[(u,v,a,b)] = c
        heappush(pq,(c,u,v,a,b))

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

INPUT_FILE = 'input17.txt'
lines = [list(map(int,l)) for l in readInputFile(INPUT_FILE)]
print(findShortestDistance(lines))