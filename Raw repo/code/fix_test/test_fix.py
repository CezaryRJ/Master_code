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



a = open("a.txt","r")

a = a.readlines()

for x in a:

    res1 = solr.search("From-address:" + fix_adr(x),**param)

    if res1.raw_response["response"]["numFound"] < 1:
        print(x)
        fix_adr(x)
        print("_")
        exit()


a = open("b.txt","r")

a = a.readlines()

for x in a:

    res1 = solr.search("From-address:" + fix_adr(x),**param)

    if res1.raw_response["response"]["numFound"] < 1:
        print(x)
        fix_adr(x)
        print("_")
        exit()


print("Test passed")
