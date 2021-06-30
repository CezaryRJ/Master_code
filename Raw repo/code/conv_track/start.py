from frame import *
from tqdm import tqdm
import codecs
import sys

codecs.register_error("strict", codecs.replace_errors)

errors = open("errors.txt","w",encoding="utf-8")

def get_parent(node,solr):

    param = {"debugQuery":"off",
    "rows" :1,
    "fl":"In-Reply-To-address"
    }

    try:
        res = solr.search("Message-ID:" + "\"" + node.id + "\"",**param)

        if res.raw_response["response"]["numFound"] == 0:

            try:
                res = solr.search("Message-ID:" + "\"" + node.id.replace(":","\:").replace("\"","\\\"") + "\"",**param)

                if res.raw_response["response"]["numFound"] == 0:
                    errors.write(node.id + "\n")
                    print("Error 1 caused by id " + node.id)
                    return list()

            except:
                errors.write(node.id + "\n")
                print("Error 2 caused by id " + node.id)
                return list()

    except:
        try:
            res = solr.search("Message-ID:" + "\"" + node.id.replace(":","\:").replace("\"","\\\"") + "\"",**param)

            if res.raw_response["response"]["numFound"] == 0:
                errors.write(node.id + "\n")
                print("Error 3 caused by id " + node.id)
                return list()

        except:
            errors.write(node.id + "\n")
            print("Error 4 caused by id " + node.id)
            return list()





    out = list()
    for x in res.raw_response["response"]["docs"][0]["In-Reply-To-address"]:

        if x in nodes:
            out.append(x)
        else:
            if ("<" + x + ">") in nodes:
                out.append("<" + x + ">")

    return out




def get_child(node,solr):

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
        res = solr.search("In-Reply-To-address:" + "\"" + node.id + "\"",**param)

        if res.raw_response["response"]["numFound"] == 0:

            if node.id[0] == "<" and node.id[-1] == ">":

                try:
                    res = solr.search("In-Reply-To-address:" + "\"" + node.id[1:][:-1].replace(":","\:") + "\"",**param)
                except:
                    errors.write(node.id + "\n")
                    print("Error 5 caused by id " + node.id)
                    return list()
            else:

                try:
                    res = solr.search("In-Reply-To-address:" + "\"" + node.id.replace(":","\:") + "\"",**param)
                except:
                    errors.write(node.id + "\n")
                    print("Error 6 caused by id " + node.id)
                    return list()


    except:

        try:
            res = solr.search("In-Reply-To-address:" + "\"" + node.id[1:][:-1].replace(":","\:") + "\"",**param)
        except:
            errors.write(node.id + "\n")
            print("Error 7 caused by id " + node.id)
            return list()




    i = 0

    out = list()


    while i < len(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"]):

        if res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i] in nodes:
            out.append(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i])


        i = i + 2

    return out




class node: #the node class
    def __init__(self, id):
        self.id = id

    parents = list()
    children = list()



solr = connect_to_solr(sys.argv[1])

slash = get_slash()

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

    nodes[ids[i]] = node(ids[i])

    i = i + 2

nodes.pop("Null")

ids = None #free memory

#i = 0
for x in tqdm(nodes):
    #print(x)
    nodes[x].parents = get_parent(nodes[x],solr)
    nodes[x].children = get_child(nodes[x],solr)

    #if len(nodes[x].parents) != 0 or len(nodes[x].children) != 0:
    #    print(x)
    #    print(nodes[x].parents)
    #    print(nodes[x].children)
#
#    i = i + 1
#    if i > 200:
#        break

out = open("tree.txt","w",encoding="utf-8")

for x in nodes:

    if len(nodes[x].parents) != 0 or len(nodes[x].children) != 0: #if there are no children or parents, skip it

        out.write(x + "\n|p" + "\n")

        for y in nodes[x].parents:
            out.write(y + "\n")

        out.write("|c\n")

        for y in nodes[x].children:
            out.write(y + "\n")

        out.write("\n\n\n")



out.close()
errors.close()
