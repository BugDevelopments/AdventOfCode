from functools import cache
INPUT_FILE = "input23.txt"

with open(INPUT_FILE) as f:
  maze = [l.strip() for l in f]

M = len(maze) # rows
N = len(maze[0]) # columns

isValid = lambda vx,vy: 0<=vx<M and 0<=vy<N 
isForest = lambda vx,vy: maze[vx][vy] == '#'
isPath = lambda vx,vy: maze[vx][vy] in '.^v><'
dirs = { (-1,0), (1,0), (0,-1), (0,1) }

def getNeighbours(vx, vy, pred=None):
  if isForest(vx,vy):
    return []
  else:
    return sorted([(vx+dx, vy+dy) for dx, dy in dirs if (vx+dx,vy+dy) != pred and isValid(vx+dx,vy+dy) and not isForest(vx+dx, vy+dy)])

# A "junction cell" in the maze is a cell that has more than 2 neighbours. Cells with exactly 2 neighbours are "hallway cells"
# We can create a smaller graph from maze whose nodes only consist of the junctions and connect the junctions by edges with weights that
# correspond to the length of the path between the junctions. 
def makeGraph(maze):
  from queue import deque

  M,N = len(maze), len(maze[0])
  isJunction = lambda x,y: len(getNeighbours(x,y))>2
  isStart = lambda x,y: (x,y)==(0,1)
  isTarget = lambda x,y: (x,y)==(M-1,N-2)
  # BFS on the maze
  graph = { (0,1):[], (M-1,N-2):[]} | { (i,j):[] for i in range(M) for j in range(N) if isJunction(i,j) }
  junctions = []
  expanded_junctions = set()
  queue = deque([(None,None,(0,1),0)]) # (junction_pred, hallway_pred,(x,y),dist)
  while len(queue):
    junction_pred,hallway_pred,node,dist = queue.popleft()

    if isJunction(*node) or isStart(*node) or isTarget(*node): # 1. case : We reached a junction 
      if junction_pred:
         if (node,dist) not in graph[junction_pred]:
          graph[junction_pred].append((node,dist))
          graph[node].append((junction_pred,dist)) 
      if node not in expanded_junctions:
        expanded_junctions.add(node)
        junctions.append(node)
        queue.extend([(node,node,(vx,vy),1) for vx,vy in getNeighbours(node[0],node[1],hallway_pred)])
    else: # 2. case : We're on a hallway
      queue.extend([(junction_pred,node,(vx,vy),dist+1) for vx,vy in getNeighbours(node[0],node[1],hallway_pred)])
  return graph, junctions

def labelGraph(graph, junctions):
  # make a dictionary between junctions and letters
  letters ="SABCDEFGHIJKLMNOPQRUVWXYZ"+"ΓΔΘΛΞΠΣΦΨΩ"+"αβγδεζηθικλμνξοπρστυφχψω"
  letters = letters[:len(junctions)-1]+'T'
  name = {v:letters[i] for i,v in enumerate(junctions)}
#  inv_name = { v:k for k,v in name.items()}
  named_graph = {name[k]:[ (name[x],l) for x,l in v] for k,v in graph.items()}
  return name, named_graph

# Using symmetric mirror paths we can half the number of paths that need to be looked at
# It suffices to look at all paths beginning with SAB.... and their mirror paths 
def mirrorPath(path):
  mirror = {'S':'S','A':'A','B':'F','F':'B','C':'K','K':'C','D':'D',
            'H':'R','R':'H','E':'G','G':'E','M':'Z','Z':'M',
             'I':'J','J':'I', 'L':'L', 'Ξ':'Y', 'Y':'Ξ',
             'V':'O', 'O':'V', 'N':'P', 'P':'N',
             'Π':'W', 'W':'Π','Γ':'Q', 'Q':'Γ', 'U':'U',
             'Σ':'Θ','Θ':'Σ', 'Δ':'X','X':'Δ',
               'Φ':'Ψ','Ψ':'Φ', 'Λ':'Λ', 'Ω':'Ω','T':'T'}
  return ''.join(map(lambda c:mirror[c],path))

def makeEdgeRelation(named_graph):
  edges = { frozenset({x,y}):l for I in named_graph.items() for x in I[0] for (y,l) in I[1]  }
  return edges


def evaluatePath(path, edges):
  from functools import reduce
  reduce(lambda acc,P: acc+edges[frozenset({P[0],P[1]})], zip(path,path[1::],0) )
  
# Idea: DFS with BFS for reachability analysis
# Before each step we make with DFS first check that the target is still reachable, so
# that we don't get stuck in dead ends

# checks if target is reachable from start within graph avoiding avoid_nodes
#@cache
def isReachable(graph,start,target,avoid_nodes):
  from queue import deque
  visited = set(avoid_nodes)
  queue = deque([start])
  while len(queue):
    node = queue.popleft()
    if node == target:
      return True # target is reachable
    visited.add(node)
    queue.extend([x for x,_ in graph[node] if x not in visited])
  return False # target not reachable

def longestPath(graph,start, target):
  path = [(start, 0, 0)]
  visited = { start }
  max_length = 0
  max_path = []
  while path:
    node, suc, length = path.pop()
    if node == target: # target reached?
      if length > max_length:
        max_length = length
        max_path = path[::]
        max_path.append((node,suc,length))
        print('new max path found:', max_length)
    else: # target not reached yet => explore successor
      visited.add(node)
      if suc < len(graph[node]): # still successors left? then explore them
        suc_node, suc_length = graph[node][suc]
        path.append((node,suc+1,length))
        if suc_node not in visited and isReachable(graph,suc_node,target,visited): # target from successor reachable?
          path.append((suc_node,0,length+suc_length))
      else:
        visited.discard(node)
  return max_length, max_path

graph, junctions = makeGraph(maze)
name, named_graph = labelGraph(graph, junctions)
max_length, max_path = longestPath(named_graph,'S','T')
print(max_length)
# 
#
# Example:
# #S#####################
# #.......#########...###
# #######.#########.#.###
# ###.....#.>B>.###.#.###
# ###^#####.#v#.###.#.###
# ###A>...#.#.#.....#...#
# ###v###.#.#.#########.#
# ###...#.#.#.......#...#
# #####.#.#.#######.#.###
# #.....#.#.#.......#...#
# #.#####.#.#.#########v#
# #.#...#...#...###...>F#
# #.#.#v#######v###.###v#             
# #...#C>.#...>E>.#.###.#
# #####v#.#.###v#.#.###.#
# #.....#...#...#.#.#...#
# #.#########.###.#.#.###
# #...###...#...#...#.###
# ###.###.#.###v#####v###
# #...#...#.#.>D>.#.>G###
# #.###.###.#.###.#.#v###
# #.....###...###...#...#
# #####################T#
# S : (0,1)  SA: 15
# A : (5,3)  AB: 22 AC: 22
# B : (3,11) 
# C : (13,5)
# D : (13,13)
# E : (19,13)
# G : (19,19)
# F : (11,21)
# Can be simplfiied to:
#  S
#  |
#  A-B-F
#  | |/|
#  | E G
#  |/|/|
#  C-D T
# with edge weights:
# SA = 16
# etc.
# or
#              S
#              |
#              A
#             / \
#            C   B
#            |\ /|
#            | D |
#            |/ \|
#            E   F
#             \ /
#              G
#              |
#              T


# SAFDBCELGKRJOZYWΘΨΛXQPUΔΓNIVMΞΠΣΦΩT
#                     S
#                     |
#                     A
#                    / \
#                   B   F
#                  / \ / \
#                 C   D   K
#                / \ / \ / \  
#               H   E   G   R
#              / \ / \ / \ / \
#             M   I   L   J   Z
#            / \ / \ / \ / \ / \
#           Ξ - V   N   P   O - Y
#           |   \ /  \ / \ /    |
#           Π -- Γ    U   Q ----W
#           |     \  / \ /      |
#           Σ ---- Δ    X ----- Θ
#           |       \  /        |
#           Φ--------Λ----------Ψ
#            \                 /
#             \               /
#              \             /
#               \           /     
#                \         /
#                 \       /
#                  \     /
#                   \   /
#                    \ /
#                     Ω
#                     |
#                     T

# S:(A,105)|
# A:(S,105)|(B,58)|(F,370)|
# B:(A,58)|(C,204)|(D,244)|
# C:(B,204)|(H,148)|(E,236)|
# D:(B,244)|(E,56)|(G,90)|(F,104)|
# E:(D,56)|(I,124)|(C,236)|(L,158)|
# F:(A,370)|(D,104)|(K,180)|
# G:(D,90)|(J,104)|(K,118)|(L,124)|
# H:(C,148)|(M,122)|(I,144)|
# I:(E,124)|(H,144)|(N,158)|(V,242)|
# J:(G,104)|(O,88)|(P,104)|(R,238)|
# K:(G,118)|(F,180)|(R,148)|
# L:(E,158)|(G,124)|(N,48)|(P,76)|
# M:(H,122)|(V,272)|(Ξ,458)|
# N:(L,48)|(I,158)|(U,108)|(Γ,248)|
# O:(J,88)|(Q,36)|(Y,168)|(Z,246)|
# P:(L,76)|(J,104)|(Q,112)|(U,144)|
# Q:(O,36)|(P,112)|(W,104)|(X,214)|
# R:(K,148)|(J,238)|(Z,112)|
# U:(N,108)|(P,144)|(X,74)|(Δ,150)|
# V:(I,242)|(M,272)|(Γ,104)|(Ξ,154)|
# W:(Q,104)|(Y,208)|(Θ,214)|
# X:(U,74)|(Q,214)|(Θ,100)|(Λ,108)|
# Y:(O,168)|(W,208)|(Z,422)|
# Z:(R,112)|(O,246)|(Y,422)|
# Γ:(N,248)|(V,104)|(Π,82)|(Δ,82)|
# Δ:(U,150)|(Γ,82)|(Σ,86)|(Λ,104)|
# Θ:(X,100)|(W,214)|(Ψ,120)|
# Λ:(X,108)|(Δ,104)|(Φ,86)|(Ψ,292)|
# Ξ:(V,154)|(M,458)|(Π,200)|
# Π:(Γ,82)|(Σ,118)|(Ξ,200)|
# Σ:(Δ,86)|(Π,118)|(Φ,196)|
# Φ:(Λ,86)|(Σ,196)|(Ω,208)|
# Ψ:(Θ,120)|(Λ,292)|(Ω,182)|
# Ω:(Φ,208)|(Ψ,182)|(T,121)|
# T:(Ω,121)|