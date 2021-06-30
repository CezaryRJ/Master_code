from urllib.request import urlopen
from sapi import *
import sys

MAX_ROWS = 2147483647

#facet parameters
#https://lucene.apache.org/solr/guide/8_6/faceting.html#Faceting-Thefacet.sortParameter

#query parameters
#https://lucene.apache.org/solr/guide/8_6/common-query-parameters.html

host ="http://localhost:8983" #/solr"

core ="clean"


param = {"q" : "Date:" + buildDateRange(["1999","09","01"],"+1MONTH"),  #"Date:[1999-09-24T17:18:40Z%20TO%201999-09-24T17:18:40Z]"
"rows" : 1}


print(buildDatePoint("1990"))

#url = buildUrl(host,core,param)

print("\n" + url + "\n")

connection = urlopen(url)
response = eval(connection.read())

printResponse(response)


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	