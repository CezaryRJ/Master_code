from frame import *
from tqdm import tqdm


class node: #the node class
    def __init__(self, id,parents,children,graph,seen):
        self.id = id
        self.parents = parents
        self.children = children
        self.graph = graph
        self.seen = seen



def calc_graph(node,graph):

    graphs[graph].append(node.id)

    #print(node.id)

    for x in node.children:

        nodes[x].graph = graph

        if nodes[x].seen == False:
            nodes[x].seen = True
            calc_graph(nodes[x],graph)


    for x in node.parents:

        nodes[x].graph = graph

        if nodes[x].seen == False:
            nodes[x].seen = True
            calc_graph(nodes[x],graph)







slash = get_slash()
reader = open(sys.argv[1],"r",encoding="utf-8")
lines = reader.readlines()

nodes_read = 0

nodes = dict()

i = 0
while i < len(lines) and lines[i] == "Δ\n":

	id = ""
	parents = list()
	children = list()

	while lines[i] != "§\n":
		i = i + 1

		while lines[i] != "λ\n":
			id = id + lines[i]
			i = i + 1

		id = id[:-1]

		i = i + 1

		if lines[i] == "Γp\n":
			i = i + 1
			while lines[i] == "α\n":
				i = i + 1
				tmp = ""
				while lines[i] != "Ω\n":
					tmp = tmp + lines[i]
					i = i + 1
				parents.append(tmp[:-1])
				i = i + 1

		if lines[i] == "Γc\n":
			i = i + 1
			while lines[i] == "α\n":
				i = i + 1
				tmp = ""
				while lines[i] != "Ω\n":
					tmp = tmp + lines[i]
					i = i + 1
				children.append(tmp[:-1])
				i = i + 1

	nodes[id] = node(id,parents,children,-1,False)


	nodes_read = nodes_read + 1

	i = i + 3
	#print(nodes[id].id)
	#print(nodes[id].parents)
	#print(nodes[id].children)
	#exit()

print("Nodes loaded from file = " + str(nodes_read))

graphs = dict()
graph_id = 0

keys = dict()

for x in nodes.keys():
    keys[x] = None

acum = 0
length = len(keys)

pbar = tqdm(total=len(keys))
while len(keys) > 0:


    start_id = list(keys.keys())[0]

    graphs[graph_id] = list()

    nodes[start_id].seen = True

    calc_graph(nodes[start_id] , graph_id)

    acum = acum + len(graphs[graph_id])
    for x in graphs[graph_id]:
        keys.pop(x)

    pbar.update(len(graphs[graph_id]))

    graph_id = graph_id + 1

    if acum > length:
        print("Something went wrong")
        exit()
