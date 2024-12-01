from collections import namedtuple
import operator
import re


# A "part" is a dictionary {'x':num_x , 'm':num_m, 'a':num_a, 's':num_s}
# and a Rule is a named tuple
# If a Rule consists only of a return label ret the other components of the tuple are set to None
Rule = namedtuple("Rule",["var","op","num","ret"])

op_table = { '<' : operator.lt , '>': operator.gt}

# applyRule(r,p) applies a rule r to a part p 
# returns the labbel r.ret for the next workflow (or the accepting 'A', rejecting 'R'), if the condition of the rule r is satisfied by the part p  
# or None if it isn't satisfied
applyRule = lambda r,p: r.ret if not r.var or r.op(p[r.var],r.num) else None

# A workflow is a list of rules wf=[r0, r1, ...]
# applyWorklow(wf,p) applies the workflow wf to the part p
# Return the first value that isn't None, i.e. the return value of the first rule r that is satisfied by p 
applyWorkflow = lambda wf,p: next(x for x in  map(lambda r: applyRule(r,p), wf) if x is not None) 


### Parse Input
INPUT_FILE = "input19.txt"
with open(INPUT_FILE) as f:
  # Parse Workflows
  workflows = dict()
  l = f.readline()
  while l != '\n':
  # workflows have the format: 'px{a<2006:qkq,m>2090:A,rfg}'
    name = re.search(r'(.*)(?={)',l).group(0)
    rules = re.findall(r'[,{](.*?)(?=[,}])',l)    
    workflows[name] = []
    for r in rules:
      if ':' in r:
        m = re.search(r'(?P<var>[xmas])(?P<op>[<>])(?P<num>\d+):(?P<ret>.*)',r)
        workflows[name].append(Rule(var=m.group('var'),op=op_table[m.group('op')],num=int(m.group('num')),ret=m.group('ret')))
      else:
        workflows[name].append(Rule(var=None,op=None,num=None,ret=r))
    l = f.readline()
  # Parse Parts
  parts = []
  # parts have the format '{x=787,m=2655,a=1222,s=2876}'
  for l in f:
    m=re.findall(r'([xmas]=\d+)',l)
    parts.append({ s[0]: int(s[2:]) for s in m})

# Apply the workflows to the parts
acc = [] # save the accepted parts here
rej = [] # save the rejected parts here
for p in parts:
  res = applyWorkflow(workflows['in'],p)
  while res not in {'A','R'}:
    res = applyWorkflow(workflows[res],p)
  if res=='A':
    acc.append(p)
  else:
    rej.append(p)
print(sum( sum(a.values()) for a in acc))