import pysolr
import sys
from frame import *

solr = connect_to_solr(sys.argv[1])

slash = get_slash()


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"author",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1
}

res = solr.search("*:*",**param)

i = 0

names = set()

names_dict = dict()

out = open("names.txt","w")

while i < len(res.raw_response["facet_counts"]["facet_fields"]["author"]):

    out.write(res.raw_response["facet_counts"]["facet_fields"]["author"][i] + "\n")

    tmp = res.raw_response["facet_counts"]["facet_fields"]["author"][i].split(" ")

    try:

        names_dict[tmp[-1]].append(tmp[:-1])

    except:
        names_dict[tmp[-1]] = list()
        names_dict[tmp[-1]].append(tmp[:-1])

    if res.raw_response["facet_counts"]["facet_fields"]["author"][i] in names:

        print(res.raw_response["facet_counts"]["facet_fields"]["author"][i])

    else:

        names.add(res.raw_response["facet_counts"]["facet_fields"]["author"][i])

    i = i + 2

out.close()

for x in names_dict:
    if len(names_dict[x]) > 1:
        print(x)
        print(names_dict[x])
