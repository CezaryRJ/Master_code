from frame import *
from tqdm import tqdm
import codecs
import sys
import datetime
import numpy

codecs.register_error("strict", codecs.replace_errors)

def time_to_day(inn):

    out = int(inn[0])/24#hours

    if inn[1][0] == "0":#minutes
        out = out + int(inn[1][1])/24/60
    else:
        out = out +  int(inn[1])/24/60

    if inn[2][0] == "0":#minutes
        out = out +  int(inn[1][1])/24/60/60
    else:
        out = out +  int(inn[1])/24/60/60

    return out



def delta_to_days(delta):

    #print(delta)

    tmp = str(delta).split(" days, ")

    if len(tmp) == 1:
        tmp = str(delta).split(" day, ")

    if len(tmp) == 1:
        return time_to_day(tmp[0].split(":"))
    else:
        return int(tmp[0]) + time_to_day(tmp[1].split(":"))



class node: #the node class

    targets = list()

    is_start = True
    is_end = True

    def __init__(self, id,parents,children,seen):
        self.id = id
        self.parents = parents
        self.children = children
        self.seen = seen

def calc_thread(start_node,node,graph,path,subgraph,max_length):

    path.append(node.id)

    node.seen = True

    if node.id in start_node.targets:
        results[graph][start_node.id][node.id] = path.copy()
        try:
            node.targets.remove(start_node.id)
        except ValueError: #several paths to a node from the samde node, cant remove twice
            pass


        for x in path:
            subgraph.add(x)
        #    print("lui")

        #print(path)
        #print(path[-2])

    if len(path) < max_length:

        for x in node.children:

            calc_thread(start_node,full_graphs[graph][x],graph,path,subgraph,max_path_length)


        for x in node.parents:

            calc_thread(start_node,full_graphs[graph][x],graph,path,subgraph,max_path_length)

    node.seen = False
    del path[-1]



def to_py_time(inn):
    return datetime.datetime(int(inn[:4]), int(inn[5:][:2]), int(inn[8:][:2]),int(inn[11:][:2]),int(inn[14:][:2]),int(inn[17:][:2]))

def order_set_date(set,solr):
    param = {"debugQuery":"off",
    "rows" :0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"Date",
    "facet.limit":1,
    "facet.sort":"count",
    "facet.mincount":1
    }

    sort = dict()

#    print(set)


    for x in set:
        res = solr.search("Message-ID:" + "\"" + x.replace(":","\:").replace("\\","\\\\") + "\"",**param)

        sort[x] = to_py_time(res.raw_response["facet_counts"]["facet_fields"]["Date"][0])

    sort_dict = sorted(sort, key=sort.get)

    out = dict()

    for x in sort_dict:
        out[x] = sort[x]

    return out










def facet_to_set(facet):

    out = set()

    i = 0

    while i < len(facet):
        out.add(facet[i])
        i = i + 2

    return out



solr = connect_to_solr(sys.argv[1])

slash = get_slash()


query_term = "(Subject :\"last call\" AND NOT Subject:\"working group last call\" AND NOT Subject:\"WGLC\")"

print("Query term = " + query_term + "\n")


start = 1990
year = start



results_mean = dict()#conv duration
results_div = dict()

results_adr = dict()

while year != 2021:

    param = {"debugQuery":"off",
    "rows" :0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"Message-ID",
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":1
    }


    res2 = solr.search(query_term + " AND Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)

    print("Subject ids found " +str(len(res2.raw_response["facet_counts"]["facet_fields"]["Message-ID"])))

    id_list = facet_to_set(res2.raw_response["facet_counts"]["facet_fields"]["Message-ID"])


    try:
        id_list.remove("Null")
    except:
        pass



    print("\nUnique ids found " + str(len(id_list)))

    max_path_length = 3

    solr_nodes = connect_to_solr("nodes")

    solr_graphs = connect_to_solr("graphs")


    param = {"debugQuery":"off",
    "rows" :0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"graph-id",
    "facet.limit":1,
    "facet.sort":"count",
    "facet.mincount":1
    }

    graph_set = dict()

    for x in tqdm(id_list): #figure out whivh graphs are relevant

        try:
            res = solr_nodes.search("node-id:" + "\"" + str(x).replace(":","\:") + "\"",**param)

            if res.raw_response["response"]["numFound"] > 0:

                try:
                    graph_set[res.raw_response["facet_counts"]["facet_fields"]["graph-id"][0]].append(x)
                except KeyError:
                    graph_set[res.raw_response["facet_counts"]["facet_fields"]["graph-id"][0]] = list()
                    graph_set[res.raw_response["facet_counts"]["facet_fields"]["graph-id"][0]].append(x)

        except:

            print(x)



    #graph_set.pop("150849")#--------------------------------------------------------------------------------------------------------------

    keys = list(graph_set.keys())


    for x in keys: #remove if length less than 2

        if len(graph_set[x]) < 2:
            graph_set.pop(x)


    #for x in graph_set: #print
    #    print(x)
    #    print(graph_set[x])


    graphs = dict()

    param = {"debugQuery":"off",
    "rows" :1
    }

    print("Getting graphs")
    for x in graph_set: #fetch all needed graphs

        res = solr_graphs.search("graph-id:" + str(x),**param)
        graphs[x] = res.raw_response["response"]["docs"][0]["nodes"]



    full_graphs = dict()

    for x in graphs:
        #print("\nLoading graph " +  str(x))
        for y in graphs[x]:
            res = solr_nodes.search("node-id:" + "\"" + str(y).replace(":","\:").replace("\"","\\\"") + "\"",**param)

            parent = list()
            child = list()


            if "parent" in res.raw_response["response"]["docs"][0].keys():
                parent = res.raw_response["response"]["docs"][0]["parent"]



            if "child" in res.raw_response["response"]["docs"][0].keys():
                child = res.raw_response["response"]["docs"][0]["child"]


            try:

                full_graphs[x][y] = node(y,parent,child,False)

            except KeyError:

                full_graphs[x] = dict()
                full_graphs[x][y] = node(y,parent,child,False)



    results = dict()
    targets = graph_set

    print("Setting targets\n")
    for x in targets:
        #print("Graph " + str(x))
        #print(targets[x])
        results[x] = dict()
        for y in targets[x]:
            full_graphs[x][y].targets = targets[x].copy()
            full_graphs[x][y].targets.remove(y)

            results[x][y] = dict()

            for z in full_graphs[x][y].targets:
                results[x][y][z] = list()


    print("Loading done\n\nCalculating threads\n\n")





    conv_length = list()

    conv_length_map = dict()

    set_adr = set()


    time = list()

    for x in tqdm(graph_set):

        subgraphs = list()



        for y in graph_set[x]:

            tmp = set()

            calc_thread(full_graphs[x][y],full_graphs[x][y],x,list(),tmp,max_path_length)

            if len(tmp) > 0:
                subgraphs.append(tmp)



        conv = list()

        del_list = dict()

        try:
            conv.append(subgraphs[0])
        except IndexError:
            pass

        while len(subgraphs) > 0:

            del_list = list()
            merged = False
            for y in conv:
                for z in subgraphs:
                    if len(y.intersection(z)) != 0:
                        y.update(z)
                        del_list.append(z)
                        merged = True




                for y in del_list:
                    subgraphs.remove(y)

            if merged == False:
                conv.append(subgraphs[0])



        #print("Conversations in graph " + str(x))
        #print("\n--------------------------------------------------------------------------------------------------------\n")

        param = {"debugQuery":"off",
        "rows" :0,
        "facet":"on", #if this is set to "off" then no facet will be returned
        "facet.field":"From-address",
        "facet.limit":-1,
        "facet.sort":"count",
        "facet.mincount":1
        }

        for z in conv:

            for a in z:
                res = solr.search("Message-ID:" +"\""+ a + "\"",**param)

                i = 0

                while i < len(res.raw_response["facet_counts"]["facet_fields"]["From-address"]):
                    set_adr.add(res.raw_response["facet_counts"]["facet_fields"]["From-address"][i])
                    i = i + 2


            conv_length.append(len(z))

            try:
                conv_length_map[len(z)] = conv_length_map[len(z)] + 1
            except:
                conv_length_map[len(z)] = 1

            tmp = order_set_date(z,solr)

            keys = list(tmp.keys())

            #print("Targets")
            #print(targets[x])
            #print("Thread")


            #print(tmp[keys[-1]] - tmp[keys[0]])
            time.append(delta_to_days(tmp[keys[-1]] - tmp[keys[0]]))

            #for y in keys[:-1]:
            #    print(y,end=" ")
            #    print(tmp[y],end="   -------->>>   ")

            #print(keys[-1], end = " ")
            #print(tmp[keys[-1]])

            #print("\n\n")



    #for x in set_adr:
    #    print(x)


    print("\n\n\nYEAR = " + str(year) + "\n\n")
    print("Conv length")

    if len(set_adr)> 0:

        results_adr[year] = len(set_adr)

        results_mean[year] = numpy.mean(time)
        results_div[year] = numpy.std(time)

        print("Mean duration (days) = " + str(results_mean[year]))
        print("STD duration (days) = " + str(results_div[year]))

        print("\n")





        print("Unique email addresses involved = " + str(len(set_adr)))

        print("Amount of conversations found = " + str(len(conv_length)))

        if len(conv_length) > 0:
            print("Average length = " + str(numpy.average(conv_length)))

            print("std div = " + str(numpy.std(conv_length)))
        else:
            print("No conv found")



    year = year + 1
    #content id 209284
    #Subject id 149432


print("\n\nDURATION\n")
print("\\addplot[color=red] coordinates {")
for x in results_mean:
    print("(" + str(x) + "," + str(results_mean[x]) + ")")

print("};\n\n")

print("\\addplot[name path=us_top,color=blue!70] coordinates {")
for x in results_mean:
    print("(" + str(x) + "," + str(results_mean[x]+((results_div[x])/2)) + ")")

print("};\n\n")

print("\\addplot[name path=us_down,color=blue!70] coordinates {")
for x in results_mean:
    print("(" + str(x) + "," + str(results_mean[x]-((results_div[x])/2)) + ")")

print("};\n\n")




print("\n\nPARTICIPANTS\n")
print("\\addplot[color=red] coordinates {")
for x in results_adr:
    print("(" + str(x) + "," + str(results_adr[x]) + ")")

print("};\n\n")
