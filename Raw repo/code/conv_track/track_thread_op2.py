from frame import *
from tqdm import tqdm
import codecs
import sys
import datetime

codecs.register_error("strict", codecs.replace_errors)

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




def get_new_date(msg_id,solr):

    param = {"debugQuery":"off",
    "rows" :1
    }

    res = solr_nodes.search("node-id:" + "\"" + x.replace(":","\:").replace("\\","\\\\") + "\"",**param)

    children_dates = list()
    parents_dates = list()

    i = 0

    for x in res.raw_response["response"]["docs"][0]["children"]:
        #the child node is now in tmp
        tmp = solr.search("Message-ID:" + "\"" + x.replace(":","\:").replace("\\","\\\\") + "\"",**param)

        date = to_py_time(tmp.raw_response["response"]["docs"][0]["date"])

        if date < datetime.date(1980, 1, 1) and datetime.date(2021, 1, 1) < date: #tmp is before
            children_dates.append(date)


    for x in res.raw_response["response"]["docs"][0]["parents"]:
        #the child node is now in tmp
        tmp = solr.search("Message-ID:" + "\"" + x.replace(":","\:").replace("\\","\\\\") + "\"",**param)

        date = to_py_time(tmp.raw_response["response"]["docs"][0]["date"])

        if date < datetime.date(1980, 1, 1) and datetime.date(2021, 1, 1) < date: #tmp is before
            parents_dates.append(date)


    start = None
    end = None

    if len(children_dates) > 0 and len(parents_dates) > 0:
        for x in children_dates:
            for y in parents_dates:
                if y < x and (y - x > start-end):
                    start = y
                    end = x

        if start != None:
            return ((start-end)/2 + end) #return the middle
        else:
            return None


    #if we only have one, just return one that is within the boundries
    elif len(children_dates) == 0 and len(parents_dates) > 0:
        for x in parents_dates:
            if x < datetime.date(1980, 1, 1) and datetime.date(2021, 1, 1) < x:
                return x

    elif len(children_dates) > 0 and len(parents_dates) == 0:
        for x in parents_dates:
            if x < datetime.date(1980, 1, 1) and datetime.date(2021, 1, 1) < x:
                return x




def order_set_date_op2(set,solr):
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

        tmp = to_py_time(res.raw_response["facet_counts"]["facet_fields"]["Date"][0])

        if tmp < datetime.datetime(1980, 1, 1,0,0,0): #tmp is before
            a = get_new_date(x,solr)

            if a != None:
                sort[x] = a

        elif datetime.datetime(2021, 1, 1,0,0,0) < tmp:# tmp is after
            a = get_new_date(x,solr)

            if a != None:
                sort[x] = a

        else:
            sort[x] = tmp





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

param = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Message-ID",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1
}

i = 3

query_term = sys.argv[2]

while i < len(sys.argv):
    query_term = query_term + " " + sys.argv[i]

    i = i + 1

query_term = "\"" + query_term + "\""

print("Query term = " + query_term + "\n")

res1 = solr.search("Content:" + query_term,**param)
res2 = solr.search("Subject:" + query_term,**param)

print("Content ids found " + str(len(res1.raw_response["facet_counts"]["facet_fields"]["Message-ID"])))
print("Subject ids found " +str(len(res2.raw_response["facet_counts"]["facet_fields"]["Message-ID"])))

id_list = facet_to_set(res1.raw_response["facet_counts"]["facet_fields"]["Message-ID"])

id_list = id_list.union(facet_to_set(res2.raw_response["facet_counts"]["facet_fields"]["Message-ID"]))


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
for x in tqdm(graph_set): #fetch all needed graphs

    res = solr_graphs.search("graph-id:" + str(x),**param)
    graphs[x] = res.raw_response["response"]["docs"][0]["nodes"]



full_graphs = dict()

for x in graphs:
    print("\nLoading graph " +  str(x))
    for y in tqdm(graphs[x]):
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
    print("Graph " + str(x))
    print(targets[x])
    results[x] = dict()
    for y in tqdm(targets[x]):
        full_graphs[x][y].targets = targets[x].copy()
        full_graphs[x][y].targets.remove(y)

        results[x][y] = dict()

        for z in full_graphs[x][y].targets:
            results[x][y][z] = list()


print("Loading done\n\nCalculating threads\n\n")




for x in graph_set:
    print(x, end= "\n\n")
    subgraphs = list()



    for y in graph_set[x]:

        tmp = set()

        calc_thread(full_graphs[x][y],full_graphs[x][y],x,list(),tmp,max_path_length)

        if len(tmp) > 0:
            subgraphs.append(tmp)



    #first find the largest graph
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



    print("Conversations in graph " + str(x))
    print("\n--------------------------------------------------------------------------------------------------------\n")
    for z in conv:
        tmp = order_set_date_op2(z,solr)

        keys = list(tmp.keys())

        print("Targets")
        print(targets[x])
        print("Thread")



        for y in keys[:-1]:
            print(y,end=" ")
            print(tmp[y],end="   -------->>>   ")

        print(keys[-1], end = " ")
        print(tmp[keys[-1]])

        print("\n\n")
