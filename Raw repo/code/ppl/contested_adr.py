from frame import *
import sys
import os
import codecs
from tqdm import tqdm
codecs.register_error("strict", codecs.replace_errors)


solr = connect_to_solr(sys.argv[1])

try:
    os.mkdir("errors")
    os.mkdir("people")
except:
    pass


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1 #can only have more than one name if more than 1 msg sendt

}


slash = get_slash()

res1 = solr.search("*:*",**param)

tmp = res1.raw_response["facet_counts"]["facet_fields"]["From-address"]

adr_list = list()

i = 0

while i < len(tmp):
    adr_list.append(tmp[i])
    i = i + 2



param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-name",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1 #can only have more than one name if more than 1 msg sendt

}

found = list()

for x in tqdm(adr_list):
    res = solr.search("From-address:" + "\"" + x + "\"",**param).raw_response["facet_counts"]["facet_fields"]["From-name"]

    if len(res) > 20:
        #print(x)
        found.append(x)

out = open("contested.txt","w")

for x in found:
    out.write(x + "\n")
