import pysolr
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sapi import *

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

param = {"debugQuery":"off",
"rows" : 0
}

start = 1980
year = start

res1 = []
res2 = []
res3 = []


#FROM ERRORS

i = 0
print("From errors\n")
while year < 2021:

	#print(str(year) + "-01-01T00:00:00Z")

	query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From:Null AND NOT (To:Null AND Cc:Null AND Bcc:Null)"

	res1.append(solr.search(query,**param))#first get a list of mailing lists

	docs = res1[i].raw_response["response"]["numFound"]

	print("Error in " + str(year) + " = " + str(docs))

	year = year + 1

	i = i + 1




i = 0
year = start
#dest errors
print("\n\n\nDestination errors\n")
while year < 2021:

	#print(str(year) + "-01-01T00:00:00Z")

	query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND NOT From:Null AND (To:Null AND Cc:Null AND Bcc:Null)"

	res2.append(solr.search(query,**param))#first get a list of mailing lists

	docs = res2[i].raw_response["response"]["numFound"]

	print("Error in " + str(year) + " = " + str(docs))

	year = year + 1
	i = i + 1




i = 0
year = start
#Botherrors
print("\n\n\nBoth errors\n")
while year < 2021:

	#print(str(year) + "-01-01T00:00:00Z")

	query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From:Null AND (To:Null AND Cc:Null AND Bcc:Null)"

	res3.append(solr.search(query,**param))#first get a list of mailing lists

	docs = res3[i].raw_response["response"]["numFound"]

	print("Error in " + str(year) + " = " + str(docs))

	year = year + 1
	i = i + 1





year = 1980
i = 0
sum = 0
print("\n\n\nLateX output\n")
while i < 41:

	query = "Date:[" + str(year+i) + "-01-01T00:00:00Z TO "+str(year+i) + "-01-01T00:00:00Z+1YEAR]"

	a = solr.search(query,**param)

	print(str(year+i) + " & " + str(res1[i].raw_response["response"]["numFound"]) + " & " + str(res2[i].raw_response["response"]["numFound"]) + " & " + str(res3[i].raw_response["response"]["numFound"]) + " & " + str(a.raw_response["response"]["numFound"]) + " & ", end = '')



	tmp = res1[i].raw_response["response"]["numFound"] + res2[i].raw_response["response"]["numFound"] + res3[i].raw_response["response"]["numFound"]
	sum = sum + tmp

	i = i + 1

	if(a.raw_response["response"]["numFound"] != 0):
		print(str('%f' % ((tmp/a.raw_response["response"]["numFound"])*100)) + "\\%" +  "\\\\\n\\hline")
	else:
		print("0.000000\\%" +  "\\\\\n\\hline")

print("\n\n\nSum = " + str(sum))
