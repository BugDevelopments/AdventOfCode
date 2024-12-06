from itertools import combinations
import re
from graphlib import TopologicalSorter

def read_input_file(input_file):
	try:
		with open(input_file, 'r') as f:
			rules, updates = f.read().split('\n\n')
			rules = {(int(x), int(y)) for x, y in re.findall(r'(\d+)\|(\d+)', rules)}
			updates = [list(map(int, u.split(','))) for u in updates.split()]
	except FileNotFoundError:
		print(f"Error: The input file '{input_file}' was not found.")
		exit(1)
	return rules, updates

def part1(rules, updates):
	def isValid(update):
		return all((y, x) not in rules for (x, y) in combinations(update, 2))

	num = sum(u[len(u) // 2] for u in updates if isValid(u))
	print("Solution to part 1:", num)

def part2(rules, updates):
	def topological_sort(nodes, rules):
		ts = TopologicalSorter()
		for u, v in rules:
			if u in nodes and v in nodes:
				ts.add(v, u)
		return list(ts.static_order())

	middle_sum = 0
	for update in updates:
		if not all((y, x) not in rules for (x, y) in combinations(update, 2)):
			sorted_update = topological_sort(set(update), rules)
			middle_page = sorted_update[len(sorted_update) // 2]
			middle_sum += middle_page

	print("Solution to part 2:", middle_sum)

def main():
	input_file = "input5.txt"
	rules, updates = read_input_file(input_file)
	part1(rules, updates)
	part2(rules, updates)

if __name__ == '__main__':
	main()
