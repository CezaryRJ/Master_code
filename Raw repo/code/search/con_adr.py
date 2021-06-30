from frame import *
import sys
from tqdm import tqdm

solr = connect_to_solr(sys.argv[1])

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":100

}

slash = get_slash()

res1 = solr.search("*:*",**param)

adr = list()

i = 0

while i < len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"]):
    adr.append(res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i])
    i = i + 2

#print(adr)

print(len(adr))

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-name",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

blacklist = dict()

for x in tqdm(adr):
    res1 = solr.search("From-address:" + x,**param)

    if len(res1.raw_response["facet_counts"]["facet_fields"]["From-name"])/2 > 100:

        blacklist[x] = len(res1.raw_response["facet_counts"]["facet_fields"]["From-name"])

for x in blacklist:
    print(x,end = " & ")
    print(blacklist[x], end = "\\\\\n")
    print("\hline\n")

print(len(blacklist))

for x in blacklist:
    print(x)
