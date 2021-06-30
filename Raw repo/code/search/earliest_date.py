import pysolr
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sapi import *

#earliest date is 1956
core = "ietf"

host = "ls.hpc.uio.no:8983"

addr = "http://cezaryrj:SolrisNice1995@" + host + "/solr/" + core + "/"

solr = pysolr.Solr(addr)



param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Date",
"facet.limit":-1,
"facet.sort":"index",
"facet.mincount":1,
"stats":"off",
"stats.field":"Mailing-list"

}

res1 = solr.search("*:*",**param)#first get a list of mailing lists

i = 0

while i < 1000:
	print(getFacet(res1)[i])
	i = i + 2



