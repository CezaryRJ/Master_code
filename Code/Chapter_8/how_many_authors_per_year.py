import pysolr
import codecs
import sys
import os
import numpy
from frame import *
from tqdm import tqdm


codecs.register_error("strict", codecs.replace_errors)



slash = "\\"

if sys.platform == "win32":
	print("\n\nRunning on Windows\n")
else:
	slash = "/"
	print("\n\nRunning on Unix\n")

try:
	print("\nUsing core " + sys.argv[1] + "\n")
except:
	print("No core name provided")
	exit()


solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

solr_authors = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/author")

start = 1990
year = start


blacklist = open("blacklist.txt","r").readlines()



while year != 2021:

	#print("\n\n" + str(year))

	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"From-address",
	"facet.limit":150,
	"facet.sort":"count",
	"facet.mincount":1
	}


	#first get addresses and stats
	stats = dict()

	res = solr.search("Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)#first get a list of mailing lists

	i = 0
	adr_list = list()
	while i < 300 and i <len(res.raw_response["facet_counts"]["facet_fields"]["From-address"]):
		adr_list.append(res.raw_response["facet_counts"]["facet_fields"]["From-address"][i].lower())

		i = i + 2

	for x in blacklist:
		for y in adr_list:
			if y == x[:-1].lower():
				adr_list.remove(y)
				break


	#print(adr_list)

	param = {"debugQuery":"off",
	"rows" : 0
	}

	sum_authors = 0

	adr_list = adr_list[100:]

	for x in adr_list:

		res = solr_authors.search("address:" + "\"" + x + "\"",**param)#first get a list of mailing lists

		if res.raw_response["response"]["numFound"] > 0:
			sum_authors = sum_authors + 1


	#print(sum_authors)
	#print(sum_authors/100)
	#print("\n")

	print("(" +str(year) + "," + str(sum_authors/100) + ")")

	year = year + 1
			#print("\nRemoved " + x + "\n")
