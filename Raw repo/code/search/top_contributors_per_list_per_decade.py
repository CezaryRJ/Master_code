import pysolr
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sapi import *

core = "ietf"

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@ls.hpc.uio.no:8983/solr/" + core + "/")


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

res1 = solr.search("*:*",**param)#first get a list of mailing lists

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":50,
"facet.sort":"count",
"facet.mincount":1

}

if not os.path.exists('Top_contributors'):
    os.makedirs('Top_contributors')

figure(num=None, figsize=(200, 15), dpi=100, facecolor='w', edgecolor='k')

x = 0
f = ""
year = 1950

while x < len(getFacet(res1)):
	if not os.path.exists("Top_contributors/" + getFacet(res1)[x]):
		os.makedirs('Top_contributors/' + getFacet(res1)[x])
		
	print(getFacet(res1)[x])
	
	while year < 2021 :
		
		
		res = solr.search("Mailing-list:" + getFacet(res1)[x] + " AND Date:" + buildDateRange(str(year),"+10YEARS"),**param)

		i = 0
		if 0 < len(getFacet(res)) :
			
			f = open("Top_contributors/" +getFacet(res1)[x] +"/" + getFacet(res1)[x] +"-top50-" + str(year) + "_to_" + str(year+10) + ".txt","w")
			f.write(str(year) + " TO " + str(year+10) + "\n") 
			f.write("-------#####------->    " + getFacet(res1)[x] + "\n")
		
			while i < len(getFacet(res)):
				f.write(getFacet(res)[i] + " " + str(getFacet(res)[i+1]) + "\n")
				i = i + 2

			f.close()
		
		
		year = year + 10
	
	
	x = x + 2
	year = 1950
	
	 
#for x in res.debug:#
#	print(x)
#	print(res.debug[x])
