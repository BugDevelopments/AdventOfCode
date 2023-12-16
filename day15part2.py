from functools import reduce

INPUT_FILE = 'input15.txt'

with open(INPUT_FILE) as f:
    inp = f.readline().strip()

instructions = inp.split(',')

hash_step = lambda acc, c:(acc+ord(c))*17 % 256
hash_value = lambda s: reduce(hash_step,s,0)

box = [[] for _ in range(256)]

def process_instruction(instruction):
  if '=' in instruction:
    label, focal_length = instruction.split('=')
    box_number = hash_value(label)
    try:
      idx = list(map(lambda x:x[0], box[box_number])).index(label)
      box[box_number][idx] = (label,focal_length)
    except:
      box[box_number].append((label,focal_length))
  elif '-' in instruction:
    label,_ = instruction.split('-')
    box_number = hash_value(label)
    try:
      idx = list(map(lambda x:x[0], box[box_number])).index(label)
      del box[box_number][idx]
    except:
      pass     
  else: 
    print(f"error: neither = nor - in ${i}")

for i in instructions:
  process_instruction(i)

print(sum( (b_nr+1)*(s_nr+1)*int(fl) for b_nr, b in enumerate(box) for s_nr,(_,fl) in enumerate(b) ))