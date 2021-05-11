from frame import *
from tqdm import tqdm
import codecs
import sys
import uploader


codecs.register_error("strict", codecs.replace_errors)


class node: #the node class
    def __init__(self, id,parents,children,graph_id,seen):
        self.id = id
        self.parents = parents
        self.children = children
        self.graph_id = graph_id
        self.seen = seen

def node_to_dict(node):
    out = dict()

    out["node-id"] = node.id
    out["graph-id"] = node.graph_id

    if len(node.parents) > 0:
        out["parent"] = list(node.parents)

    if len(node.children) > 0:
        out["child"] = list(node.children)


    return out


def calc_graph(node,graph_id,graph):

    node.graph_id = graph_id
    node.seen = True
    graph.add(node.id)

    for x in node.children:

        if nodes[x].seen == False:

            calc_graph(nodes[x],graph_id,graph)


    for x in node.parents:

        if nodes[x].seen == False:

            calc_graph(nodes[x],graph_id,graph)


def get_parent(node_inn,solr):

    param = {"debugQuery":"off",
    "rows" :0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"In-Reply-To-ID",
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":1
    }

    try:
        res = solr.search("Message-ID:" + "\"" + node_inn.id + "\"",**param)

        if res.raw_response["response"]["numFound"] == 0:

            try:
                res = solr.search("Message-ID:" + "\"" + node_inn.id.replace(":","\:").replace("\"","\\\"") + "\"",**param)

                if res.raw_response["response"]["numFound"] == 0:

                    print("Error 1 caused by id " + node_inn.id)
                    errors.write("1\n " + node_inn.id + "\n|\n\n")
                    return set()

            except:

                print("Error 2 caused by id " + node_inn.id)
                errors.write("2\n" + node_inn.id + "\n|\n\n")
                return set()

    except:
        try:
            res = solr.search("Message-ID:" + "\"" + node_inn.id.replace(":","\:").replace("\"","\\\"") + "\"",**param)

            if res.raw_response["response"]["numFound"] == 0:

                print("Error 3 caused by id " + node_inn.id)
                errors.write("3\n" + node_inn.id + "\n|\n\n")
                return set()

        except:

            print("Error 4 caused by id " + node_inn.id)
            errors.write("4\n" + node_inn.id + "\n|\n\n")
            return set()





    i = 0

    while i < len(res.raw_response["facet_counts"]["facet_fields"]["In-Reply-To-ID"]):

        if res.raw_response["facet_counts"]["facet_fields"]["In-Reply-To-ID"][i] in nodes:

            #print("\n")
            #print(node_inn.id)

            #print(res.raw_response["facet_counts"]["facet_fields"]["In-Reply-To-ID"][i])

            node_inn.parents.add(res.raw_response["facet_counts"]["facet_fields"]["In-Reply-To-ID"][i])

            nodes[res.raw_response["facet_counts"]["facet_fields"]["In-Reply-To-ID"][i]].children.add(node_inn.id)


        i = i + 2







def get_child(node_inn,solr):

    param = {"debugQuery":"off",
    "rows" :0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"Message-ID",
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":1
    }
    #print(node.id)
    try:
        #print(node.id[1:][:-1])
        res = solr.search("In-Reply-To-ID:" + "\"" + node_inn.id + "\"",**param)

        if res.raw_response["response"]["numFound"] == 0:

            if node_inn.id[0] == "<" and node_inn.id[-1] == ">":

                try:
                    res = solr.search("In-Reply-To-ID:" + "\"" + node_inn.id[1:][:-1].replace(":","\:") + "\"",**param)
                except:

                    print("Error 5 caused by id " + node_inn.id)
                    errors.write("5\n" + node_inn.id + "\n|\n\n")
                    return set()
            else:

                try:
                    res = solr.search("In-Reply-To-ID:" + "\"" + node_inn.id.replace(":","\:") + "\"",**param)
                except:

                    print("Error 6 caused by id " + node_inn.id)
                    errors.write("6\n" + node_inn.id + "\n|\n\n")
                    return set()


    except:

        try:
            res = solr.search("In-Reply-To-ID:" + "\"" + node_inn.id[1:][:-1].replace(":","\:") + "\"",**param)
        except:

            print("Error 7 caused by id " + node_inn.id)
            errors.write("7\n" + node_inn.id + "\n|\n\n")
            return set()




    i = 0

    while i < len(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"]):

        if res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i] in nodes:

            #print("\n")
            #print(node_inn.id)

            #print(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i])

            node_inn.children.add(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i])

            nodes[res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i]].parents.add(node_inn.id)


        i = i + 2







solr = connect_to_solr(sys.argv[1])

slash = get_slash()

errors = open("errors.txt","w",encoding="utf-8")

param = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Message-ID",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1
}

res = solr.search("*:*",**param)

i = 0

ids = res.raw_response["facet_counts"]["facet_fields"]["Message-ID"]

nodes = dict()


while i < len(ids):

    nodes[ids[i]] = node(ids[i],set(),set(),-1,False)

    i = i + 2

try:
    nodes.pop("Null")
except:
    pass


ids = None #free memory
#
i = 0
for x in tqdm(nodes):

    get_parent(nodes[x],solr)
    get_child(nodes[x],solr)


    #if len(nodes[x].parents) != 0 or len(nodes[x].children) != 0:
    #    print(x)
    #    print(nodes[x].parents)
    #    print(nodes[x].children)
#
#    i = i + 1
#    if i > 200:
#        break


out = open("t" + slash + "nodes.txt","w",encoding="utf-8")
report = open("Report.txt","w")

roots = dict()

del_list = list()

acum = 0
print("Printing to file")
for x in tqdm(nodes):

    #print(nodes[x].id)
    #print(nodes[x].parents)
    #print(nodes[x].children)


    if len(nodes[x].parents) != 0 or len(nodes[x].children) != 0: #if there are no children or parents, skip it

        if len(nodes[x].parents) == 0:
            roots[nodes[x].id] = None



        out.write("Δ\n" + x + "\nλ\nΓp" + "\n")

        for y in nodes[x].parents:
            out.write("α\n" + y + "\nΩ\n")

        out.write("Γc\n")

        for y in nodes[x].children:
            out.write("α\n" + y + "\nΩ\n")

        out.write("§\n\n\n")

        acum = acum + 1

    else:

        del_list.append(nodes[x].id)

report.write("Ammount of nodes written = " + str(acum) + "\n")
print("Ammount of nodes written = " + str(acum))


print("Deleting empty nodes")
for x in tqdm(del_list):
    del nodes[x]



out.close()
errors.close()

print("Calculating graphs")



graph_id = 0

keys = dict()

for x in nodes.keys():
    keys[x] = None

acum = 0
length = len(keys)

nodes_for_solr = list()
graphs_for_solr = list()

graph_counter = 0

pbar = tqdm(total=len(keys))
while len(keys) > 0:


    start_id = list(keys.keys())[0]

    nodes[start_id].seen = True

    graph_nodes = set()

    calc_graph(nodes[start_id] , graph_id,graph_nodes)


    #tmp = list()
    for x in graph_nodes:
        nodes_for_solr.append(node_to_dict(nodes[x]))
        keys.pop(x)

    #nodes_for_solr.append(tmp)

    tmp = dict()

    tmp["graph-id"] = graph_id
    tmp["nodes"] = list(graph_nodes)

    graphs_for_solr.append(tmp)

    acum = acum + len(graph_nodes)

    pbar.update(len(graph_nodes))

    graph_id = graph_id + 1


print("Graphs found = " + str(graph_id))

#print(nodes_for_solr)
print("Acum = " + str(acum))
print("length = " + str(length))
if acum != length:
    print("Something went wrong")



print("\n\nUploading nodes")
solr = connect_to_solr("nodes")

uploader.upload(solr,nodes_for_solr)



print("\n\nUploading graphs")
solr = connect_to_solr("graphs")

uploader.upload(solr,graphs_for_solr)
