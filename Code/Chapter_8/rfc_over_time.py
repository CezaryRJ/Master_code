from frame import *
import sys
from tqdm import tqdm


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"date",
"facet.limit":-1,
"facet.sort":"value",
"facet.mincount":1

}

slash = get_slash()
solr = connect_to_solr("rfc")

res1 = solr.search("*:*",**param)

dates = dict()



i = 0

while i < len(res1.raw_response["facet_counts"]["facet_fields"]["date"]):
    dates[res1.raw_response["facet_counts"]["facet_fields"]["date"][i]] = res1.raw_response["facet_counts"]["facet_fields"]["date"][i+1]

    i = i + 2

#print(dates)

for x in dates:

    if str(x[5:][:-14]) == "0":
        print("(" +  str(int(str(x[:4])) + (1/12)*int(x[6:][:-13])) + "," + str(dates[x]) + ")", end = "")
    else:
        print("(" +  str(int(str(x[:4])) + (1/12)*int(x[5:][:-13])) + "," + str(dates[x]) + ")", end = "")
