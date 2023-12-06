def main():
  # open input file and save as list of lines
  input_file = 'input5.txt'
  try:
    with open(input_file) as f:
        lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    return

  # parse input lines and save as list of seeds and list of maps
  seeds = list(map(int,lines[0].split(':')[1].split()))
  maps = []
  for l in lines[1:]:
    if l == '': 
      continue
    if l[-1] == ':':
      maps.append([])     
    else:
      maps[-1].append(list(map(int,l.split())))

  # compute map(x)
  def apply(map, x):
    for dst,src,ran in map:
      if src<=x<src+ran:
        return dst+x-src
    return x

  # compute the location of each seed
  locations = []
  for s in seeds:
    for m in maps:
      s = apply(m,s)
    locations.append(s)

  print(min(locations))

if __name__ == '__main__':
  main()