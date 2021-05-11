import pysolr
import sys
#“,+,-,/,!,[,],{,},^,~
#+,-,~,!

class node: #the node class
    def __init__(self,id,parents,children):
        self.id = id
        self.parents = parents
        self.children = children


def fix_adr(inn):
    #print(inn)
    out = ""
    for x in inn:

        if x == "\"":
            out = out + "\\"

        out = out + x

    out = out.strip()
    #print( "\"" + out + "\"")
    return  "\"" + out + "\""

def get_slash():
    slash = "\\"

    if sys.platform == "win32":
    	print("\n\nRunning on Windows\n")
    else:
    	slash = "/"
    	print("\n\nRunning on Unix\n")

    return slash

def connect_to_solr(core):
    try:
        return pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + core)
    except:
        print("Could not connect to core " + core)
        exit()



def load_nodes(file_location):

    lines = open(file_location,"r",encoding="utf-8").readlines()

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

    	nodes[id] = node(id,parents,children)

    	nodes_read = nodes_read + 1

    	i = i + 3
    	#print(nodes[id].id)
    	#print(nodes[id].parents)
    	#print(nodes[id].children)
    	#exit()

    print("Nodes loaded from file = " + str(nodes_read))

    return nodes
