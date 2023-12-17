from heapq import heappush, heappop
from itertools import product
from math import inf
from os import read


norm = lambda x: 0 if x==0 else x//abs(x)

# usind dijkstra algorithm to find the shortest distance between two nodes 
def findShortestDistance(G):
  m,n = len(G),len(G[0])
  dirs = {(0,1),(0,-1),(1,0),(-1,0)}
  directions = {(i*x,i*y) for i in range(1,4) for x,y in dirs}
  dist = { (x,y,i,j): inf for i,j in product(range(m),range(n)) for x,y in directions } 
  
  isValid = lambda x,y,i,j: 0<=i<m and 0<=j<n and (x,y) in directions

  nb = lambda x,y,i,j: { (a,b,i+norm(a),j+norm(b)) for a,b in { (norm(y),norm(x)), 
                                                     (norm(-y),norm(-x)), 
                                                     (x+norm(x),y+norm(y))
                                                     } if isValid(a,b,i+norm(a),j+norm(b)) } if not i==j==0 else {(0,1,0,1) , (1,0,1,0)}

  pq = [] # priority queue
  heappush(pq,(0,0,0,0,0))

  while pq:
    d,x,y,i,j = heappop(pq)
    if (i,j)==(m-1,n-1):
      print(d)
      break
    for (u,v,a,b) in nb(x,y,i,j):
      c = d+G[a][b]
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