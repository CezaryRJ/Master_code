from frame import *
from tqdm import tqdm


class node: #the node class
    def __init__(self, id,parents,children,level,seen):
        self.id = id
        self.parents = parents
        self.children = children
        self.level = level
        self.seen = seen



def calc_level(node,level,root):


    for x in node.children:

        nodes[x].level[root.id] = level

        if nodes[x].seen == False:
            nodes[x].seen = True
            calc_level(nodes[x],level+1,root)
            nodes[x].seen = False







slash = get_slash()
reader = open( "D:\\nodes.txt","r",encoding="utf-8")
lines = reader.readlines()

nodes_read = 0

nodes = dict()

roots = list()

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

	nodes[id] = node(id,parents,children,dict(),False)
	nodes_read = nodes_read + 1

	if len(parents) == 0:
		roots.append(id)


	i = i + 3
	#print(nodes[id].id)
	#print(nodes[id].parents)
	#print(nodes[id].children)
	#exit()

print("Nodes loaded from file = " + str(nodes_read))
print("Roots = " + str(len(roots)))
print(len(nodes))



print(list(nodes.keys())[0])

print(list(nodes.keys())[len(nodes.keys())-1])


for x in tqdm(roots):
	calc_level(nodes[x],1,nodes[x]) #all roots are level 0

#verify

for x in tqdm(roots):

	if len(nodes[x].level) > 0:
		print("error")
		exit()

	elif len(nodes[x].level) > 1:
		print(x)

out = open("t" + slash + "done.txt","w",encoding="utf-8")

for x in tqdm(nodes):
	out.write("Δ\n" + x + "\nλ\nΓp" + "\n")

	for y in nodes[x].parents:
		out.write("α\n" + y + "\nΩ\n")

	out.write("Γc\n")

	for y in nodes[x].children:
		out.write("α\n" + y + "\nΩ\n")

	out.write("Γl\n")

	for y in nodes[x].level:
		out.write("α\n" + y + "\nΩ " + str(nodes[x].level[y]) + "\n")

	out.write("§\n\n\n")

out.close()

#for x in nodes:
#
#	if len(nodes[x].level) > 0:
#		print(x)
#		print(nodes[x].level)
#		exit()
