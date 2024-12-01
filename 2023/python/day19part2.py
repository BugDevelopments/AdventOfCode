from collections import namedtuple
import math
import operator
import re

Rule = namedtuple("Rule",["var","op","num","ret"])
op_table = { '<' : operator.lt , '>': operator.gt}
workflows = dict()

### Parse Input
INPUT_FILE = "input19.txt"
with open(INPUT_FILE) as f:
  # Parse Workflows
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

# Idea:
# The workflows correspond to nodes in a decision tree. 
# Each rule r of a workflow decides what combinations go to the child-node labeled by r.ret
# and what combinations are passed on to the next rule of the workflow. 
# We give the decision tree not a single combination but a set of combinations as input.
# Each rule then sends subsets of the input set to the child nodes.
# Represent the input sets as intervals:
# Intervals:
# I = { 'x': [low_x,up_x] , 'm': [low_m, up_m] , 'a': [low_a, up_a], 's': [low_s, up_s] }
# For each variable the interval represents the set of values that the variable can have
# open intervals: low_x<x<up_x
# 

# Input intervals In 
# Output intervals Out=[Out_true, Out_false]
# Out_true are the intervals that satisfy the rule
# Out_false are the intervals that don't satisfy the rule (and are then send to the next rule of the workflow)
def applyRuleToIntervals(r,In):
  Out_true =  { k:list(v) for k,v in In.items()} # deep copy
  Out_false = { k:list(v) for k,v in In.items()} # deep copy

  # r.op is None, i.e. all combinations satsify the rule
  if not r.op:
    return [In,[]]
  # r.op is '<'
  if r.op == operator.lt:   
    Out_true[r.var][1] = min(In[r.var][1],r.num) # adopt upper bound
    Out_false[r.var][0] = max(In[r.var][0],r.num-1) # adopt lower bound >=
  # r.op is '>' 
  elif r.op:
    Out_true[r.var][0] = max(In[r.var][0],r.num) # adopt lower bound
    Out_false[r.var][1] = max(In[r.var][0],r.num+1) # adopt upper bound <=
  # return empty list if one the intervals is empty 
  Out = [Out_true, Out_false]
  Out = [ I if I[r.var][0]<I[r.var][1] else [] for I in Out]
  return Out

# Inpute: intervals In
# Output: number of combinations accepted from this node/workflow wf of the decision tree 
def applyWorkflowToIntervals(wf,In):
  num_A = 0
  In_r = [[], {k:list(v) for k,v in In.items()}] # deep copy
  for r in workflows[wf]:
    In_r = applyRuleToIntervals(r,In_r[1])
    if r.ret=='A': # accepting node?
      num_A += math.prod(v[1]-v[0]-1 for v in In_r[0].values())
    elif r.ret!='R': # not rejecting nor accepting node? => recursion
      num_A += applyWorkflowToIntervals(r.ret,In_r[0])
  return num_A

I_all = { 'x': [0,4001], 'm': [0,4001], 'a': [0,4001], 's': [0,4001] }
print(applyWorkflowToIntervals('in',I_all))