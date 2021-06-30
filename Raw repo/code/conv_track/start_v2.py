from frame import *
from tqdm import tqdm
import codecs
import sys

codecs.register_error("strict", codecs.replace_errors)

class msg_node: #the node class
    def __init__(self,id,a,b):
        self.id = id
        self.parents = a
        self.children = b








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

    while i < len(res.raw_response["facet_counts"]["facet_fields"]["Message-ID"]):

        if res.raw_response["facet_counts"]["facet_fields"]["Message-ID"][i] in nodes:

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

    nodes[ids[i]] = msg_node(ids[i],set(),set())

    i = i + 2

nodes.pop("Null")


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


out = open("tree.txt","w",encoding="utf-8")


acum = 0
for x in nodes:

    #print(nodes[x].id)
    #print(nodes[x].parents)
    #print(nodes[x].children)

    if len(nodes[x].parents) != 0 or len(nodes[x].children) != 0: #if there are no children or parents, skip it

        acum = acum + 1

        out.write(x + "\n|p" + "\n")

        for y in nodes[x].parents:
            out.write(y + "\n|\n")

        out.write("|c\n")

        for y in nodes[x].children:
            out.write(y + "\n|\n")

        out.write("\n\n\n")


report = open("Report.txt","w")

report.write("Ammount of nodes written = " + str(acum) + "\n")
print("Ammount of nodes written = " + str(acum))



out.close()
report.close()
errors.close()
