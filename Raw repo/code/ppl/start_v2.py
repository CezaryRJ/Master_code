from frame import *
import sys
import os
import codecs
import spacy
from tqdm import tqdm
codecs.register_error("strict", codecs.replace_errors)


solr = connect_to_solr(sys.argv[1])

nlp = spacy.load("en_core_web_sm")


error_list = list()

try:
    os.mkdir("errors")
    os.mkdir("people")
except:
    pass


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-name",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":2 #can only have more than one name if more than 1 msg sendt

}





slash = get_slash()

res1 = solr.search("*:*",**param)

tmp = res1.raw_response["facet_counts"]["facet_fields"]["From-name"]

tmp_list = list()



i = 0

while i < len(tmp):
    tmp_list.append(tmp[i])
    i = i + 2



try:
    tmp_list.remove("Null")
except:
    print("No Null value found")




param_name = {"debugQuery":"off",
"rows" : 2147483647,
"fl" : "From-name" ,
"facet":"off"
}

param_adr = {"debugQuery":"off",
"rows" : 2147483647,
"fl" : "From-address" ,
"facet":"off"
}




name_list = list()

removed = list()

for y in tmp_list:
    n = nlp("\"" + y + "\"")
    for x in n.ents:
        if x.label_ == "PERSON" or x.label_ == "ORG":
            name_list.append(x.text)
        else:
            print("\n" + str(y))
            print(x.text + " " + x.label_)
            removed.append(x.text + " " + x.label_)


print(len(name_list))
print(len(removed))

out = open("name_list.txt","w")
for x in name_list:
    out.write(x + "\n")
out.close()

out = open("removed.txt","w")
for x in removed:
    out.write(x + "\n")
out.close()

agents = list()

print(str(len(tmp_list)) + " addresses found")
