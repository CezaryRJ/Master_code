from frame import *
import sys
from tqdm import tqdm
import numpy

solr = connect_to_solr("graphs")

param = {"debugQuery":"off",
"rows" : 214748364
}

slash = get_slash()

res1 = solr.search("*:*",**param)

sizes = list()

dist = dict()

for x in tqdm(res1.raw_response["response"]["docs"]):

    sizes.append(len(x["nodes"]))
    #print(len(x["nodes"]))

    try:
        dist[len(x["nodes"])] = dist[len(x["nodes"])] + 1
    except:
        dist[len(x["nodes"])] = 1

print(numpy.mean(sizes))
print(numpy.std(sizes))

dictionary_items = dist.items()

sorted_items = sorted(dictionary_items)

#print(sorted_items)

print("NORMAL \n\n\n")

sum = 0

for x in sorted_items:
    print("(" + str(x[0]) + "," + str(x[1]) + ")",end = "")
    sum = sum + x[1]



print("cdf \n\n\n")


tmp = 0
for x in sorted_items:
    tmp = tmp + x[1]
    print("(" + str(x[0]) + "," + str(tmp/sum) + ")",end = "")
