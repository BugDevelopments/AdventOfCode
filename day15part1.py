from functools import reduce

INPUT_FILE = 'input15.txt'

with open(INPUT_FILE) as f:
    inp = f.readline().strip()

hash_step = lambda acc, c:(acc+ord(c))*17 % 256
print(sum(reduce(hash_step,l,0) for l in inp.split(',')))