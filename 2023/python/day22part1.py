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

def isDisintegrable(b, supports, supportedBy):
  """Check whether the removal of brick b with support graph `supports` and its inverse `supportedBy` will lead to bricks falling down."""
  return all( len(supportedBy[x])>1  for x in supports[b])

def solvePart1():
  """Solves Part 1: compute the number of disintegrable bricks and prints out this number"""
  supports = applyGravity(bricks)
  supportedBy = { x:[k for k,v in supports.items() if x in v] for x in range(len(bricks)) } # the inverse of supports
  print(sum(1 for b in range(len(bricks)) if isDisintegrable(b,supports,supportedBy)))

solvePart1()