from collections import deque

c_current = "red"
c_child = "green"
c_visited = "black"
visited = []
adj_list = []
result = deque()

def dfs(node):
	try:
		visited[node] = 1
	except IndexError:
		return
	global result, c_current, c_child, c_visited
	result.append([node + 1, c_current])
	for neighbor in adj_list[node]:
		if visited[neighbor] == 0:
			result.append([neighbor + 1, c_child])
			dfs(neighbor)
	result.append([node + 1, c_visited])

def get_actions(no_nodes, no_edges, edges):
	global visited, adj_list
	visited = [0 for i in range(0, no_nodes)]
	adj_list = [[] for i in range(0, no_nodes)]
	for edge in edges:
		x = edge[0] - 1
		y = edge[1] - 1
		adj_list[x].append(y)
		adj_list[y].append(x)
	dfs(0)
	global result
	return result

