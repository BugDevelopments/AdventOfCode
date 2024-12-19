import time
from multiprocessing import Pool, cpu_count

# A map_configuration has a map with a starting position and a guard on the map with a position and direction
class map_configuration:
  ## class attributes ##
  map = None # the guard's map 
  start_position = None # the start position of the guard that is denoted by the '^'-character on the map

  ## class methods ##
  @classmethod
  def set_map(cls,map):
    cls.map = map
    cls.start_position = cls.get_start_position_on_map()

  @classmethod
  def get_start_position_on_map(cls):
    return next((i,j) for (i,j) in cls.map if cls.map[(i,j)]=='^')

  @classmethod
  def set_map_from_file(cls,input_file):
    try:
      with open(input_file, 'r') as f: 
        map = { (i,j):char for i,line in enumerate(f.read().split()) for j,char in enumerate(line) }
        cls.set_map(map)
    except FileNotFoundError:
      print(f"Error: The input file '{input_file}' was not found.")
      exit(1)

  ## instance methods ##
  # instances of map_configuration put a guard on the map, that has  a position, direction and optionally a set of obstructions   
  def __init__(self,guard_position=None, guard_direction=(-1,0),obstructions=None):
    if guard_position is None:
      self.guard_position = self.__class__.start_position
    else:
      self.guard_position = guard_position
    self.guard_direction = guard_direction
    if obstructions is None:
      self.obstructions = set()
    else:
      self.obstructions = obstructions

  # let the guard turn by 90° clockwise
  def make_turn(self):
    self.guard_direction = {(-1,0):(0,1), (0,1):(1,0), (1,0):(0,-1), (0,-1):(-1,0)}[self.guard_direction]

  # let the guard turn around until he points into a direction that isn't blocked and then take a step forward 
  def make_step(self):
    next_position = (self.guard_position[0]+self.guard_direction[0], self.guard_position[1]+self.guard_direction[1])
    if self.map.get(next_position) != '#' and next_position not in self.obstructions:
      self.guard_position = next_position 
    else:
      self.make_turn()
      self.make_step()

  def guard_is_on_map(self):
    return self.guard_position in self.map

# return the set of all positions the guard visits on the map when following his walking routine until he steps outside the map
def get_path(map_c):
  path = set()
  while map_c.guard_is_on_map():
    path.add(map_c.guard_position)
    map_c.make_step()
  return path

def part1():
  map_c = map_configuration()

  print("Solution for part 1:",len(get_path(map_c)))    

# check if the guard's walking routine leads him into a cycle
def cycleCheck(map_c):
    visited = set()     
    while map_c.guard_is_on_map():
        if (map_c.guard_position, map_c.guard_direction) in visited:
            return True
        visited.add((map_c.guard_position, map_c.guard_direction))
        map_c.make_step()
    return False

# this is needed for multiprocessing under windows, which uses spawn() instead of fork() so that subprocesses don't inherit the global variables of the parent process
def initialize_map(preloaded_map):
    map_configuration.set_map(preloaded_map)

def part2():
    map_c = map_configuration()
    # we only need to check points on the path the guard walks, not on positions the guard never reaches anyway
    points_to_check = get_path(map_c)-{map_configuration.start_position}

    # using multiprocessing
    # Determine the number of processes to use (leave one core free for the system)
    num_processes = max(1, cpu_count() - 1)
    print(f"Using {num_processes} processes for part 2")
    # number of points each process checks
    chunk_size = len(points_to_check) // num_processes + 1 

    # use a pool of processes running cycleCheck with different obstructions in parallel
    args = [map_configuration(obstructions={obs}) for obs in points_to_check]
    with Pool(
        processes=num_processes,
        initializer=initialize_map,
        initargs=(map_configuration.map,)
    ) as pool:
        results = pool.map(cycleCheck, args, chunksize=chunk_size)

    cycleCount = sum(results)
    print("Solution to part 2:", cycleCount)


def main():
  input_file = "input6.txt"
  map_configuration.set_map_from_file(input_file)

  part1()
  start_time = time.time()
  part2()
  end_time = time.time()

  print(f"Execution time for part 2: {end_time-start_time} seconds")

if __name__ == '__main__':
  main()