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
  lines = [list(map(lambda x:int(x) if x.isdigit() else {'R':(0,1), 'L':(0,-1),'U':(-1,0), 'D':(1,0)}[x],l.split()[:2])) for l in f]  


# A "scanline" is a list [x0,y0,x1,y1, ... , xn,yn] with xi<=yi  and yi<x_i+1  representing the union of closed intervals
# [xi,yi]
  
scanline_length = lambda SL: sum( y-x+1 for x,y in zip(SL[::2],SL[1::2]))

# insert new segment into scanline
# SL=[x0,y0,x1,y2,...,xn,yn]=[z0,z1,z2,...] (strictly increasing sequence x0<y0<x1<y1<..)
# c<d must be between xi<=c<d<=yi for a i or between yi<=c<d<=x_i+1

#  I) xi<=c<d<=yi  ~ z_2n<=c<d<=z_2n+1
# 4 cases:    replace _  by  _
# 1. xi<c<d<yi : (xi,yi) -> (xi,c) (d,yi) (replace (xi,yi) by 2 tuples ~ insert c and d)
# 2. xi=c<d<yi : (xi,yi) -> (d,yi) (replace xi by d ~ delete c)
# 3. xi<c<d=yi : (xi,yi) -> (xi,c) (replace yi by c ~ delete d=yi)
# 4. xi=c<d=yo : (xi,yi) -> () delete (delete xi=c, yi=d) 
# corresponds to set(SL)^set({c,d})
# II) yi<=c<d<=x_i+1 ~ z_2n+1<=c<d<=z_2n+2
# 4 cases:
# 1. yi<c<d<x_i+1 : insert c and d
# 2. xi=c<d<yi :    delete c=xi
# 3. xi<c<d=yi :    delete d=yi
# 4. xi=c<d=yo :    delete xi=c, yi=d
#
# So in both cases it's just set(SL) ^ {c,d} (^=XOR)
#def scanline_insert(SL0,c,d):
#  return set(SL0)^{c,d}
#
# Due to the commutativity of ^ we can also just XOR with all corners on a line
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
  #print("new row:",row)
  area += edge_rest(SL,row)
  #print("added edge rest",area)
  area += scanline_length(SL)*(i-last_i)
  #print("added scanline area", area)
  SL = scanline_insert(SL,row)
  #print("scanline",SL)
  #print("new scanline:",SL)
  last_i = i
  #print("scanline:",SL)

print("area:",area)