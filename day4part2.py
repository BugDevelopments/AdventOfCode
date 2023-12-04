def main():
  # open input file and save its lines
  input_file = 'input4.txt'
  try:
    with open(input_file) as f:
       lines = [l.strip() for l in f]
  except FileNotFoundError:
    print(f"Error opening input file '{input_file}': FileNotFoundError")
    return

  cards = [[c.split() for c in l.split(':')[1].split('|')] for l in lines]
  score = [ sum((x in c[0]) for x in c[1]) for c in cards]
  num_cards = []
  # compute number of cards using the recursion formula:
  # num_cards[n] = (num_cards[n-1]*(score[n-1]>=1)+(num_cards[n-2]*(score[n-2]>=2)+...+(num_cards[0]*(score[0]>=n)+1 
  for n in range(len(cards)):
    num_cards_n = sum( (num_cards[i]*(score[i]>=n-i)) for i in range(n))+1
    num_cards.append(num_cards_n)
  res = sum(num_cards)
  print(res)
  
if __name__ == "__main__":
  main()