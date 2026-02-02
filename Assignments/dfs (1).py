

from adjacency_list_graph import AdjacencyListGraph

WHITE = 0  # undiscovered
GRAY = 1   # discovered
BLACK = 2  # visited


def dfs(G, start_dfs_tree=None, discover_func=None, finish_func=None, order=None):
	"""Perform depth-first search on a graph represented by adjacency lists.

	Arguments:
	G -- a graph, represented by adjacency lists.
	start_dfs_tree -- parameterless function called upon discovering the first vertex in a
	depth-first tree.  Defaults to do nothing.
	discover_func -- function called upon discovering a vertex from traversing
	an edge in a graph, taking the vertex as an argument.  Defaults to do nothing.
	finish_func -- function called upon finishing a vertex in a graph, taking the
	vertex as an argument.  Defaults to do nothing.
	order -- order of vertices in starting searches.  Defaults to the numerical order
	of the vertices.

	Returns:
	d -- list of vertex discovery times
	f -- list of vertex finish times
	pi -- list of depth-first vertex predecessors
	"""
	# Initialize color, pi, distance, and finish time lists.
	global time, color, pi, d, f
	time = 0  # global timestamp
	card_V = G.get_card_V()
	color = [WHITE] * card_V  # vertices are numbered, color[0] corresponds with color of vertex 0.
	pi = [None] * card_V
	d = [None] * card_V 	# discovery times
	f = [None] * card_V 	# finish times

	# Default order for starting searches goes from vertex 0 to vertex (card_V - 1).
	if order is None:
		order = range(card_V)

	# Visit each unvisited vertex.
	for u in order:
		if color[u] == WHITE:
			if start_dfs_tree is not None:
				start_dfs_tree()
			if discover_func is not None:
				discover_func(u)  # discover first vertex in this depth-first tree
			dfs_visit(G, u, discover_func, finish_func)  # DFS from vertex u
	return d, f, pi


def dfs_visit(G, u, discover_func, finish_func):
	"""Perform depth-first search on a graph represented by adjacency lists, starting
	from a given vertex.

	Arguments:
	G -- a graph, represented by adjacency lists.
	u -- root of the depth-first tree
	discover_func -- function called upon discovering a vertex from traversing
	an edge in a graph, taking the vertex as an argument.  Defaults to do nothing.
	finish_func -- function called upon finishing a vertex in a graph, taking the
	vertex as an argument.  Defaults to do nothing.

	Updates the global timestamp time and the global lists color, pi, d, and f.
	"""
	global time, color, pi, d, f
	time += 1  # white vertex u has just been discovered
	d[u] = time
	color[u] = GRAY

	for edge in G.get_adj_list(u):  # explore each edge (u, v)
		v = edge.get_v()
		if color[v] == WHITE:
			if discover_func is not None:
				discover_func(v)  # do something with vertex v upon discovering it
			pi[v] = u
			dfs_visit(G, v, discover_func, finish_func)
	time += 1
	f[u] = time
	color[u] = BLACK  # black u; it is finished
	if finish_func is not None:
		finish_func(u)  # do something with vertex v upon finishing it


# Testing
if __name__ == "__main__":

	import numpy as np 

	# Textbook example.
	vertices = ['u', 'v', 'x', 'y', 'w', 'z']
	edges = [('u', 'v'), ('u', 'x'), ('v', 'y'), ('w', 'y'),
			 ('w', 'z'), ('x', 'v'), ('y', 'x'), ('z', 'z')]
	graph1 = AdjacencyListGraph(len(vertices))
	for edge in edges:
		graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]))
	print(graph1.strmap(lambda i: vertices[i]))
	d, f, pi = dfs(graph1)
	for v in range(len(vertices)):
		print(vertices[v] + ": d = " + str(d[v]) + ", f = " + str(f[v]) + ", pi = ", end='')
		if pi[v] is None:
			print(pi[v])
		else:
			print(vertices[pi[v]])
