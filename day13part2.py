import numpy as np

INPUT_FILE = 'input13.txt'

def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

def makeBinaryMatrix(M):
  assert(all(len(M[0])==len(m) for m in M)) # all rows need to have equal length
  return np.array([[mij=='#' for mij in mi] for mi in M])

def hasSmudge(M,r,axis=0):
  M = M.swapaxes(0,axis)
  assert(0<r<M.shape[1])
  m=min(M.shape[1]-r,r)
  res = (np.fliplr(M[:,r-m:r]) == M[:,r:r+m])
  return np.size(res)-np.count_nonzero(res)==1

def getSmudgeNumber(M):
  for r in range(1,M.shape[1]):
    if hasSmudge(M,r):
      return r
  
  for r in range(1,M.shape[0]):
    if hasSmudge(M,r,axis=1):
      return 100*r
  
lines = readInputFile(INPUT_FILE)
I = [-1]
I.extend([i for i,l in enumerate(lines) if l==''])
I.extend([len(lines)])
print(sum(getSmudgeNumber(makeBinaryMatrix(lines[i+1:j]))   for i,j in zip(I[0:], I[1:])))