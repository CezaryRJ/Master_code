import pysolr
from uploader import *
from frame import *
import sys




class node: #the node class
    def __init__(self, id,parents,children,graph):
        self.id = id
        self.parents = parents
        self.children = children
        self.graph = graph

def node_to_dict(node):

    out = dict()
    out["node-id"] = node.id
    out["parents"] = node.parents
    out["child"] = node.children
    out["graph"] = node.graph

    return out

solr = connect_to_solr(sys.argv[1])

id = "iuhiuh"
p = ["iuhi","uyguyg","iuhuih"]
c = ["hiuh","fdsdfgdfg","fdhfdgh"]

g = 44
i = 0
m = list()
a = node("iuhgkiuyyhguiky",p,c,g)

m.append(node_to_dict(a))
m.append(node_to_dict(a))

upload(solr,m)
