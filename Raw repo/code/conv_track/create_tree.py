import sys
from frame import *
from tqdm import tqdm


class node: #the node class
    def __init__(self, id,parents,children,root,level,seen):
        self.id = id
        self.parents = parents
        self.children = children
        self.root = root
        self.level = level
        self.seen = seen




def calc_level(node,level,root,index):


    try:
        tree[level].append(node.id)
    except KeyError:
        tree[level] = list()
        tree[level].append(node.id)


    if len(node.children) == 0:
        global max_lvl
        if level > max_lvl:
            global max_index
            max_lvl = level
            max_index = index
            #print(max_lvl)
    else:

        for x in node.children:

            try:
                nodes[x].level[root.id] = level

                if nodes[x].seen == False:

                    nodes[x].seen = True
                    calc_level(nodes[x],level+1,root,index)
                    nodes[x].seen = False
            except:
                errors.write(x + "\n\n")






def read_file(filename):

    a = open(filename,"r")

    a = a.readlines()

    nodes = dict()

    i = 0

    roots = list()

    while i < len(a):

        id = ""

        while a[i] != "|p\n":

            id = id + a[i]
            i = i + 1

        id = id.strip()


        i = i + 1
        parents = list()
        while a[i] != "|c\n":
            tmp = ""
            while a[i] != "|\n":
                tmp = tmp + a[i]
                i = i + 1

            parents.append(tmp[:-1])
            i = i + 1

        i = i + 1

        children = list()
        while a[i] != "\n":
            tmp = ""
            while a[i] != "|\n":
                tmp = tmp + a[i]
                i = i + 1

            children.append(tmp[:-1])
            i = i + 1

        i = i + 3


        #if i > 100:
#
#            for x in nodes:
#                print(x.id)
#                print(x.parents)
#                print(x.children)
#                print("\n")
#
#            exit()


        if len(parents) == 0:



            nodes[id] = node(id,parents,children,True,dict(),False)

            test_print.write(nodes[id].id + "\n")

            roots.append(id)
        else:
            nodes[id] = node(id,parents,children,False,dict(),False)

        #print(nodes[id].id)
        #print(nodes[id].parents)
        #print(nodes[id].children)



    return nodes,roots


test_print = open("a.txt","w")

slash = get_slash()

errors = open("tree_builder_errors.txt","w")

print("Reading file\n")

nodes,roots = read_file(sys.argv[1])

#sys.setrecursionlimit(sys.maxsize)

print(str(len(nodes)) + " nodes read from file")

max_lvl = 0
max_index = 0

out = None

i = 0

out = open("t" + slash + "trees.txt","w")

for x in tqdm(roots):

    tree = dict()

    nodes[x].seen = True
    calc_level(nodes[x],0,nodes[x],i)
    nodes[x].seen = False



    out.write("---" + str(i) + "\n")

    for y in sorted (tree.keys()) :
        out.write("\n" + str(y) + "\n")

        for z in tree[y]:
            out.write(str(z) + "\n|\n")

    out.write("\n\n\n\n\n")

    i = i + 1

out.close()
errors.close()

print("Max level")
print(max_lvl)
print(max_index)
