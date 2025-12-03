def parseInput(fileName):
    f = open(fileName)
    I = [l.strip() for l in f.readlines()]
    return I

def solvePart1(I):
    dv = { 'L' : -1 , 'R' : 1}
    cur=prev=50
    zeroes = 0
    for X in I:
        d, n = X[0], int(X[1:])
        prev = cur
        cur = (cur+dv[d]*n)%100 
        if cur==0:
            zeroes += 1
    print(zeroes)

def solvePart2(I):
    dv = { 'L' : -1 , 'R' : 1}
    cur=prev=50
    zeroes = 0
    for X in I:
        d, n = X[0], int(X[1:])
        prev = cur
        cur += dv[d]*n
        zeroes += cur//100 if cur > 0 else -cur//100+(prev!=0) 
        cur %= 100
    print(zeroes)
    
def main():
    I = parseInput("input1.txt")
    solvePart1(I)
    solvePart2(I)

if __name__ == "__main__":
    main()

