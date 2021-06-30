from sapi import *
import os
import sys

def calc_contr(solr,resinn): 
	
	facet = getFacet(resinn)
	
	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"From-address",
	"facet.limit":50,
	"facet.sort":"count",
	"facet.mincount":1

	}
	folder_name = "Top_contributors"
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)
	
	i = 0
	while i < len(facet):
	
	
		sys.stdout = open(folder_name + "/" + facet[i] + "-top-20" + ".txt", 'w') #redirect stdout to file
	
		res = solr.search("Mailing-list:" + facet[i],**param)#first get a list of mailing lists
		
		
		top = getFacet(res)
		x = 0
		while x < len(top):
			sys.stdout.write(top[x] + " " + str(top[x+1]) + "\n")
			x = x + 2
		
		sys.stdout.close()
		
		i = i + 2