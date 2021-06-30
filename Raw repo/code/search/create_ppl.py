import pysolr
import os
from sapi import *

core = "ietf"

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@ls.hpc.uio.no:8983/solr/" + core + "/")


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-name",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

res1 = solr.search("*:*",**param)#first get a list of mailing lists

param = {"debugQuery":"off",
"rows" : MAX_ROWS,
"facet":"off", #if this is set to "off" then no facet will be returned
"facet.field":"From-name",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}


if not os.path.exists('People'):
    os.makedirs('People')


x = 2 #most people are anon, so they do not count, therfore skip


name = {}

while x < len(getFacet(res1)):
	
	
	testname = "\"" + getFacet(res1)[x] + "\""
	
	#unfortunetly this needs to be done as windows wont allow files with those chars in name
	#and the fields in solr are not that clean
	filename = getFacet(res1)[x].replace("\"","").replace("/""","").replace(":","").replace("*","").replace("?","").replace("<","").replace(">","").replace("|","")
	#print(filename)
	print("Search term = " + testname)
	print("Filename    = " + filename)
	
	f = open("People/" + filename + ".txt","w")
	
	res  = solr.search("From-name:" + testname,**param)#first get a list of mailing lists
	
	name[testname] = set([])
	
	for q in res :
	
		if len(q["From-address"]) == 1:
		
			name[testname].add(q["From-address"][0])
		

	f.write(testname.replace("\"","") + "\n\n")
	for n in name[testname]:
		f.write(n + "\n")
		
	
	f.close()
	x = x + 2
	#exit()

	
	 
#for x in res.debug:#
#	print(x)
#	print(res.debug[x])
