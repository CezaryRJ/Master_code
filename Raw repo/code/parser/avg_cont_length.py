import pysolr
import os
import codecs
import sys

codecs.register_error("strict", codecs.replace_errors)

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

print("\nUsing core " + sys.argv[1] + "\n")

param = {"debugQuery":"off",
"rows" : 2147483647,
"fl":"Content",
"facet":"off", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

tmp = solr.search("*:*",**param).raw_response["response"]["docs"]

print(len(tmp))
exit()

sum = 0

for x in tmp:
    sum = sum + len(x)

print("Avarage for core " + sys.argv[1] + " is " + (sum/len(tmp)))
