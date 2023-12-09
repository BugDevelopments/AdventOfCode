def readInputFile(input_file):
  try:
    with open(input_file) as f:
        return [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    exit(-1)

def diff(L):
  return [y-x for x,y in zip(L,L[1:])]

def iszero(L):
  return all(x==0 for x in L)

def alldiff(L):
  res = [L]
  while not iszero(res[-1]):
    res.append(diff(res[-1]))
  return res

def predict(L):
  return sum(l[-1] for l in alldiff(L))

INPUT_FILE = "input9.txt"
lines = [list(map(int,l.split())) for l in readInputFile(INPUT_FILE)]

predictions = [predict(l) for l in lines]
print(sum(predictions))