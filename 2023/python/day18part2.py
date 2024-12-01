# [(x,y),nr]
def getCorners(lines):
  corners = []
  cur_loc = (0,0)
  for dir,cnt in lines:
    cur_loc = (cur_loc[0]+dir[0]*cnt, cur_loc[1]+dir[1]*cnt)
    corners.append(cur_loc)
  return corners

INPUT_FILE = "input18.txt"
with open(INPUT_FILE) as f:
  lines = []
  for l in f:  
    _,_,z = l.split()
    z,x = z[2:7], z[7] 
    x={'0':(0,1), '1':(1,0),'2':(0,-1),'3':(-1,0)}[x]
    z=int(z,base=16)
    lines.append([x,z])

scanline_length = lambda SL: sum( y-x+1 for x,y in zip(SL[::2],SL[1::2]))

def scanline_insert(SL0,R):
  return sorted(set(SL0)^set(R))

def edge_rest(SL,R):
  res = 0
  for c,d in zip(R[::2],R[1::2]):
    for x,y in zip(SL[::2],SL[1::2]):
      if d<x: # c,d must be in an odd interval
        break
      if x<=c and d<=y: # then it must hold that x<=c<d<=y
        res += d-c-1+(x==c)+(y==d)
        break
  return res

C=sorted(getCorners(lines))
SL=[] # The first scanline is just the empty set
RowIndexes = sorted({x[0] for x in C})
area = 0
last_i = 0
for i in RowIndexes:
  row = [x[1] for x in C if x[0]==i]
  area += edge_rest(SL,row)
  area += scanline_length(SL)*(i-last_i)
  SL = scanline_insert(SL,row)
  last_i = i

print("area:",area)