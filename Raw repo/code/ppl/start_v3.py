from frame import *
import sys
import os
import codecs
from tqdm import tqdm
codecs.register_error("strict", codecs.replace_errors)


solr = connect_to_solr(sys.argv[1])#connect to solr



param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-name",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":2 #can only have more than one name if more than 2 msg sendt

}


error_list = list()

try:
    os.mkdir("errors")
    os.mkdir("people")
except:
    pass



slash = get_slash()

res1 = solr.search("*:*",**param)

tmp = res1.raw_response["facet_counts"]["facet_fields"]["From-name"]

name_list = list()

i = 0
while i < len(tmp):
    name_list.append(tmp[i])
    i = i + 2



param_adr = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1 #can only have more than one name if more than 2 msg sendt

}

agents = list()

print(str(len(name_list)) + " addresses found")

name_list.remove("Null")
#print(name_list)

index = 0

iter = 0
for x in tqdm(name_list): #for each name do the following

    #print(x)
    cur_name = set()
    cur_name.add(x)

    cur_adr = set()

    res = None

    try:
        res = solr.search("From-name:" + "\"" + x + "\"",**param_adr)
    except:
        print(x)
        res = solr.search("From-name:" + "\"" + x.replace(":","\:").replace("\"","\\\"") + "\"",**param_adr)

    new_adr = set()

    i = 0

    while i < len(res.raw_response["facet_counts"]["facet_fields"]["From-address"]):
        new_adr.add(res.raw_response["facet_counts"]["facet_fields"]["From-address"][i])
        i = i + 2

    new_adr = new_adr.difference(cur_adr)

    cur_adr |= new_adr

    out = open("people" + slash + str(index) + ".txt","w",encoding="utf-8")
    for x in cur_name:
        out.write(str(x) + "\n")

    out.write("\n")

    for x in cur_adr:
        out.write(str(x) + "\n")

    out.close()

    index = index + 1
