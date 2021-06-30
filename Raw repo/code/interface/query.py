from frame import *
import sys

solr = connect_to_solr(sys.argv[1])

param = {"debugQuery":"off",
"rows" : 0,
"facet":"off", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

slash = get_slash()

res1 = solr.search(sys.argv[2],**param)

print(res1.raw_response["response"]["numFound"])
