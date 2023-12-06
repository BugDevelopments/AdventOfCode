def main():
  # open input file and save as list of lines
  input_file = 'input5.txt'
  try:
    with open(input_file) as f:
        lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")

  # parse input lines and save as list of seeds and list of maps
  seeds = list(map(int,lines[0].split(':')[1].split()))
  # re-arrange as pairs (seed, range)
  seeds = list(zip(seeds[::2],seeds[1::2]))

  # extract maps from input
  maps = []
  for l in lines[1:]:
    if l == '': 
      continue
    if l[-1] == ':':
      maps.append([])     
    else:
      maps[-1].append(list(map(int,l.split())))

  # represent intervals by pairs of number
  # the pair (src, ran) represents the interval [src,src+ran)

  # compute the set intersection of intervals I and J
  # the result is an interval again
  def intersect(I,J):
    hi_low  = max(I[0],J[0])
    low_hi = min(sum(I),sum(J))
    if hi_low >= low_hi: # intersection is empty
      return None
    else:
      return (hi_low, low_hi-hi_low)

  # compute the set difference I\J of intervals I and J 
  # the result is a list of intervals whose union is I\J 
  def minus(I,J):
    if not J:
      return [I]
    ilo,ihi = I[0],sum(I)
    jlo,jhi = J[0],sum(J)
    if jlo<=ilo and ihi<=jhi:
      return None
    if jlo>ilo:
      if ihi>jhi:
        return [(ilo,jlo-ilo), (jhi,ihi-jhi)]    
      else:
        return [(ilo,min(ihi,jlo)-ilo)]
    else:
        return [(max(ilo,jhi),ihi-max(ilo,jhi))]
  
  # argument L is a list of intervals
  # return a list of disjoint intervals whose union is equal to the union of intervals in L
  def union(L):
    if len(L)==0:
      return []
    res = []
    L=sorted(L,key=lambda x: x[0])
    cur = L[0]
    for i in range(1,len(L)):
      lo0,hi0=cur[0],sum(cur)
      lo1,hi1=L[i][0],sum(L[i])
      if lo1<=hi0:
        cur = (lo0,max(hi0,hi1)-lo0)
      else:
        res.append(cur)
        cur = L[i]
    res.append(cur)
    return res

  # computes map(I), for a list of intervals I
  # the result is a list of intervals again
  def image(map, IList):
    input_intervals = IList
    output_intervals = []
    for dst,src,ran in map:
      B=(src,ran)
      new_input_intervals = []
      for J in input_intervals:
        S = intersect(J,B)
        D = minus(J,S)
        if S:
          output_intervals.append( (dst+S[0]-src,S[1]) )
        if D:
          new_input_intervals.extend(D)
      input_intervals = union(new_input_intervals)
    output_intervals.extend(input_intervals)
    return output_intervals
  
  # compute the image of each seed interval, then choose the minimum
  Images = []
  for s in seeds:
    Im = [s]
    for m in maps:
      Im = union(image(m,Im))
    Images.append(Im)
  
  print(min(min(i[0] for i in Im) for Im in Images))

if __name__ == '__main__':
  main()