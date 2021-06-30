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

    out["node_id"] = node.id
    out["graph_id"] = node.graph_id

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
    "rows" :1,
    "fl":"In-Reply-To-address"
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



    try:
        res.raw_response["response"]["docs"][0]["In-Reply-To-address"].remove("Null")
    except:
        pass


    for x in res.raw_response["response"]["docs"][0]["In-Reply-To-address"]:

        if x in nodes:

            node_inn.parents.add(x)
            nodes[x].children.add(node_inn.id)


        else:

            if ("<" + x + ">") in nodes:

                node_inn.parents.add("<" + x + ">")
                nodes["<" + x + ">"].children.add(node_inn.id)





def check_id(node_inn,solr): #helper method for get child

    param = {"debugQuery":"off",
    "rows" :10,
    "facet":"off",
    "fl": "In-Reply-To-address" #if this is set to "off" then no facet will be returned
    }

    res1 = solr.search("In-Reply-To-address:" + "\"" + res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i].replace(":","\:") + "\"",**param)

    for x in res1.raw_response["response"]["docs"]:
        for y in x:
            if node_inn.id == x[y]:
                return True


    return False


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
        res = solr.search("In-Reply-To-address:" + "\"" + node_inn.id + "\"",**param)

        if res.raw_response["response"]["numFound"] == 0:

            if node_inn.id[0] == "<" and node_inn.id[-1] == ">":

                try:
                    res = solr.search("In-Reply-To-address:" + "\"" + node_inn.id[1:][:-1].replace(":","\:") + "\"",**param)
                except:

                    print("Error 5 caused by id " + node_inn.id)
                    errors.write("5\n" + node_inn.id + "\n|\n\n")
                    return set()
            else:

                try:
                    res = solr.search("In-Reply-To-address:" + "\"" + node_inn.id.replace(":","\:") + "\"",**param)
                except:

                    print("Error 6 caused by id " + node_inn.id)
                    errors.write("6\n" + node_inn.id + "\n|\n\n")
                    return set()


    except:

        try:
            res = solr.search("In-Reply-To-address:" + "\"" + node_inn.id[1:][:-1].replace(":","\:") + "\"",**param)
        except:

            print("Error 7 caused by id " + node_inn.id)
            errors.write("7\n" + node_inn.id + "\n|\n\n")
            return set()




    i = 0

    print(len(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"]))

    while i < len(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"]):

        if res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i] in nodes:

            tmp = check_id(node_inn,solr)

            if tmp == True:

                node_inn.children.add(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i])
                nodes[res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i]].parents.add(node_inn.id)


        i = i + 2
        print(i)







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

nodes.pop("Null")


ids = None #free memory
#
i = 0



#get_parent(nodes["<@localhost>"],solr)
get_child(nodes["<@localhost>"],solr)


#print(nodes["<@localhost>"].parents)
print(nodes["<@localhost>"].children)

exit()

    #if len(nodes[x].parents) != 0 or len(nodes[x].children) != 0:
    #    print(x)
    #    print(nodes[x].parents)
    #    print(nodes[x].children)
#
#    i = i + 1
#    if i > 200:
#        break
