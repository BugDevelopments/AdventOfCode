words = { "one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9}

def get_digits(s):
  def get_num(order=1):
    R = range(len(s))
    if order<0:
      R = reversed(R)

    for i in R:
      if s[i].isdigit():
        return int(s[i])
      
      for w in words:
        if s[i:].startswith(w):
          return words[w]
  return 10*get_num()+get_num(-1)

def main():
  input_file = 'input1.txt'
  try:
    with open(input_file) as f:
       lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    return
  print(sum(get_digits(l) for l in lines))

if __name__ == "__main__":
  main()