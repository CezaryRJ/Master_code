from frame import *
import sys
from tqdm import tqdm


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"name",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

slash = get_slash()
solr = connect_to_solr("author")

res1 = solr.search("*:*",**param)

authors = list()

i = 0

while i < len(res1.raw_response["facet_counts"]["facet_fields"]["name"]):
    authors.append(res1.raw_response["facet_counts"]["facet_fields"]["name"][i])
    i = i + 2



solr_rfc = connect_to_solr("rfc")




param = {"debugQuery":"off",
"rows" : 0
}

results = dict()

for x in tqdm(authors):
    res = solr_rfc.search("author:" + "\"" + x + "\"",**param)

    results[x] = res.raw_response["response"]["numFound"]


sort_dict = dict(sorted(results.items(), key=lambda item: item[1]))

i = 1
for x in reversed(list(sort_dict.keys())):

    print(str(i) + " & " + str(x) + " & " + str(sort_dict[x]) + "\\\\\n\\hline\n")

    if i == 20:
        break

    i = i + 1
