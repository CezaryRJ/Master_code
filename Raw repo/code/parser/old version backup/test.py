import pysolr
import os
import codecs
import sys

codecs.register_error("strict", codecs.replace_errors)

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

print("\nUsing core " + sys.argv[1] + "\n")

param = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

tmp = solr.search("*:*",**param).raw_response["facet_counts"]["facet_fields"]["Mailing-list"]


print(len(tmp)/2)
