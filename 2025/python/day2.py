
import math
import sympy

def sumStringSquares(a,b):
    '''Returns the sum of all string-squares in the interval [a,b]'''
    lena = max(1,len(str(a))//2)
    lenb = len(str(b))//2
    #print(f"{lena=},{lenb=}")
    total = 0
    for k in range(lena, lenb+1):
        lo = math.ceil(a/(10**k+1))
        hi = math.floor(b/(10**k+1))
        s = sum(s*(10**k+1) for s in range(10**(k-1),10**k) if lo<=s<=hi)
        #print(f"{lo=},{hi=},{s=}")
        total += s
    return total

def parseInput(filename):
    '''Returns the list of pairs (a,b)'''
    f = open(filename,'r')
    input_string = f.read()
    input_pairs=[x.split('-') for x in input_string.split(',')]
    return [(int(a),int(b)) for a,b in input_pairs]
 
def isStringPower(x):
    '''Checks if x is a string-power'''
    x=str(x)
    for d in sympy.divisors(len(x))[:-1]:
        if x==x[:d]*(len(x)//d):
            return True
    
    return False

def sumStringPowers(a,b):
    '''Returns the sum of all string-powers in the interval [a,b]'''
    lena = max(1,len(str(a)))
    lenb = len(str(b))
    total = 0
    for n in range(lena, lenb+1):
        divs = sympy.divisors(n)[:-1]
        for d in divs:
            seed = sum(10**(i*d) for i in range(n//d))
            lo=math.ceil(a/seed)
            hi=math.floor(b/seed)
            if 10**d<=hi-lo:
                s = sum(x*seed for x in range(10**(d-1),10**d) if lo<=x<=hi and not isStringPower(x))
            else:
                s = sum(x*seed for x in range(lo,hi+1) if x in range(10**(d-1),10**d) and not isStringPower(x))
            total += s
    return total

def sumAllStringSquares(input_pairs):
    '''Returns the sum of all string-squares in the union of the intervals given by input_pairs'''
    return sum(sumStringSquares(int(a),int(b)) for (a,b) in input_pairs)

def sumAllStringPowers(input_pairs):
    '''Returns the sum of all string-powers in the union of the intervals given by input_pairs'''
    return sum(sumStringPowers(int(a),int(b)) for (a,b) in input_pairs)

def solve():
    filename='input2.txt'
    input_pairs=parseInput(filename)
    print(f"part 1: {sumAllStringSquares(input_pairs)}")
    print(f"part 2: {sumAllStringPowers(input_pairs)}")

if __name__=='__main__':
    solve()