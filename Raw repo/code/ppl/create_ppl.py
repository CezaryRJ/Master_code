from frame import *
import sys
from tqdm import tqdm

slash = get_slash()

class person:
    def __init__(self, id,names,addresses,rfc_name):
        self.id = id
        self.rfc_name = rfc_name
        self.names = names
        self.addresses = addresses



ppl = dict()

file = open("ppl.txt","r",encoding="utf-8").readlines()

id = 0

adr_sum = 0

i = 0
while i < len(file):

    name = file[i][:-1]

    ppl[name] = person(id,set(),set(),name)

    ppl[name].names.add(file[i][:-1])

    i = i + 1

    while file[i] != "\n":
        ppl[name].addresses.add(file[i][:-1])
        i = i + 1

    adr_sum = adr_sum + len(ppl[name].addresses)





    #if len(ppl[name].addresses) > 1:
    #    print(ppl[name].id)
    #    print(ppl[name].names)
    #    print(ppl[name].addresses)


    id = id + 1
    i = i + 2

print("Names read = " + str(len(ppl)))
print("Adr read = " + str(adr_sum))



tmp = open("blacklist.txt","r").readlines()

blacklist = list()

for x in tmp:
    blacklist.append(x[:-1])


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":2

}

solr = connect_to_solr(sys.argv[1])


for x in tqdm(ppl):

    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"From-address",
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":2

    }


    res = solr.search("From-name:" + "\"" + ppl[x].rfc_name + "\"", **param)

    facet = res.raw_response["facet_counts"]["facet_fields"]["From-address"]

    i = 0

    while i < len(facet):

        if facet[i] not in blacklist:
            ppl[x].addresses.add(facet[i])

        i = i + 2






    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"From-name",
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":2

    }




    for y in ppl[x].addresses:

        res = solr.search("From-address:" +  y, **param)

        facet = res.raw_response["facet_counts"]["facet_fields"]["From-name"]

        i = 0

        while i < len(facet):
            #print(facet[i])
            ppl[x].names.add(facet[i])

            i = i + 2



out = open("ppl_new.txt","w",encoding="utf-8")

for x in ppl:

    out.write(x + "\n")
    out.write(str(ppl[x].id) + "\n\n")

    for y in ppl[x].names:
        out.write(y + "\n")

    out.write("\n")

    for y in ppl[x].addresses:
        out.write(y + "\n")

    out.write("\n\n\n")

out.close()
