import bisect

# Parse input filee
INPUT_FILE = 'input22.txt'
bricks = [] # each brick consists of a start- and endpoint with 3 coordinates x,y,z 
with open(INPUT_FILE) as f:
  for l in f:
    P1,P2 = l.strip().split('~')
    P1,P2 = list(map(int,P1.split(','))),list(map(int,P2.split(',')))
    bricks.append([P1,P2] if P1[2]<P2[2] else [P2,P1]) # sort the endpoints of each by their z-coordinates

def intervalsIntersect(I,J):
  """Check whether the closed real number intervals I and J have a common element."""
  return max(I) >= min(J) and max(J) >= min(I)

def rectsIntersect(R,S): 
  """Check whether the projections of two bricks onto the x-y plane have a common point."""
  return intervalsIntersect((R[0][0],R[1][0]),(S[0][0],S[1][0])) and intervalsIntersect((R[0][1],R[1][1]),(S[0][1],S[1][1]))

def isBelow(B,C):
  """Check whether a brick B is somewhere below another brick C."""
  return B[1][2]<C[0][2] and rectsIntersect(B,C)

def isOn(B,C):
  """Check whether brick B lies on top of brick C"""
  return C[1][2]==B[0][2]-1 and rectsIntersect(B,C)

def applyGravity(bricks):
  """Adjust the z-coordinates of the bricks after they have dropped onto the ground level z=1 and return the support graph.
    The support graph is a dictionary mapping each brick index to the list of all indices of bricks that lie on top of it.""" 
  supports = { i:[] for i in range(len(bricks)) } # support graph 

  dropped_bricks = [] # contains the dropped bricks  sorted by their upper z-coordinate in decreasing order
  sorted_bricks = sorted([i for i in range(len(bricks))], key=lambda i: bricks[i][0][2])  # sort bricks by their lower z-coordinates

  for b in sorted_bricks:
    B = bricks[b]
    try: 
      # 1. Find the first dropped brick below B with the highest z-coordinate
      c = next(c for c in dropped_bricks if isBelow(bricks[c],B) ) # throws exception if no such brick exists => brick falls on ground
      C = bricks[c]
      # drop B on C
      fall_distance = B[0][2]-C[1][2]-1
      B[0][2] -= fall_distance
      B[1][2] -= fall_distance
      bisect.insort_left(dropped_bricks,b,key=lambda b:-bricks[b][1][2])
      # 2. Update support graph for the bricks on which B now lies  
      try:
        for c in (c for c in dropped_bricks if isOn(B,bricks[c])):
          supports[c].append(b)
      except:
        pass
    except: # brick drops on the ground level z=1
      fall_distance = B[0][2]-1
      B[0][2] -= fall_distance
      B[1][2] -= fall_distance
      bisect.insort_left(dropped_bricks,b,key=lambda b:-bricks[b][1][2])  
  return supports

def solvePart2():
  """Solves Part 2: compute the sum of the number of bricks that will fall when a brick disintegrats for all bricks"""
  supports = applyGravity(bricks)
  supportedBy = { x:[k for k,v in supports.items() if x in v] for x in range(len(bricks)) } 

  supportNumbers = [0]*len(bricks)
  for k,v in supportedBy.items():
    supportNumbers[k] = len(v)

  def countFalls(start_b):
    """returns how many bricks fall when start_b is disintegrated"""
    sn = supportNumbers[::] # sn[b] is the number of bricks that support b
    numFallen = -1
    stack = [start_b] # stack of bricks that will fall/distintegrate , starting with start_b
    visited = set() # set of already seen bricks
    while stack:      # doing a depth-first search in the support graph starting from start_b 
      i = stack.pop() 
      if i in visited: # brick already visited? => Continue with next brick on the stack
        continue
      visited.add(i)   # otherwise mark it as "visited" 
      numFallen += 1   # add 1 brick that will fall
      for j in supports[i]: # decrease the number of supporting bricks for each brick on top by 1
        sn[j] -= 1
        if sn[j] <= 0 and j not in visited: # if no more bricks support j, push j onto the fall stack
          stack.append(j)
    return numFallen

  print(sum(countFalls(i) for i in range(len(bricks))))

solvePart2()