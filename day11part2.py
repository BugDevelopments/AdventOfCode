def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

INPUT_FILE = "input11.txt"

lines = readInputFile(INPUT_FILE)
M,N = len(lines), len(lines[0])
expanded_rows = [i for i in range(M) if all(lines[i][j]=='.' for j in range(N))]
expanded_cols = [j for j in range(N) if all(lines[i][j]=='.' for i in range(M))]

# Manhattan Distance + weights for the expanded rows and cols
def distance(P,Q):
  m0, M0 = min(P[0],Q[0]), max(P[0],Q[0])
  m1, M1 = min(P[1],Q[1]), max(P[1],Q[1])
  d = abs(P[0]-Q[0])+abs(P[1]-Q[1])
  d += sum(999999 for i in expanded_rows if i in range(m0+1,M0))
  d += sum(999999 for j in expanded_cols if j in range(m1+1,M1))
  return d

galaxies = [(i,j) for i in range(M) for j in range(N) if lines[i][j]=='#']
print(sum( distance(P,Q) for P in galaxies for Q in galaxies if P<Q))