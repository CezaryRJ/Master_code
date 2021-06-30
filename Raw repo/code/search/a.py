import pysolr
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sapi import *

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/ietf-archive")


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1,
"stats":"on",
"stats.field":"Date"

}

res1 = solr.search("*:*",**param)#first get a list of mailing lists

i = 0

while i < 100 :
	print(getFacet(res1)[i] + " " + str(getFacet(res1)[i+1]))
	i = i+2
