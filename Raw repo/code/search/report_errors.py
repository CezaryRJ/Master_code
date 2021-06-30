import pysolr
import os
import sys
from sapi import *


def report_errors(addr):

	folder_name = "Error_report"

	solr = pysolr.Solr(addr)


	param = {"debugQuery":"off",
	"rows" : MAX_ROWS,
	"facet":"off", #if this is set to "off" then no facet will be returned
	"facet.field":"Mailing-list",
	"facet.limit":-1,
	"facet.sort":"count",
	"facet.mincount":1

	}

	if not os.path.exists(folder_name):
		os.makedirs(folder_name)

	res1 = solr.search("From:Null",**param)#first get a list of mailing lists

	i = 0


	for x in res1.docs :
		#print(x["Mailing-list"])
		if not os.path.exists(folder_name + "/" + x["Mailing-list"]):
			os.makedirs(folder_name	+ "/" + x["Mailing-list"])
		
		
		sys.stdout = open(folder_name + "/" + x["Mailing-list"] + "/" + x["Mailing-list"] +"-email-" + str(i) + ".txt", 'w') #redirect stdout to file
		
		try:
			cnt =  x["Content"][0]
			del x["Content"]
		except:
			pass
		
		for y in x:
		
			sys.stdout.write(y + " : ")
			
		
			sys.stdout.write(str(x[y]) + "\n")
			
			
		
		sys.stdout.write("\nContent : \n\n" + cnt)
		
		sys.stdout.close()
		
		sys.stdout = open(folder_name + "/" + x["Mailing-list"] + "/" + x["Mailing-list"] +"-email-" + str(i) + "-error" + ".txt", 'w') #redirect stdout to file
		
		if cnt == "\n\n":
			sys.stdout.write("Empty file")
		else:
			sys.stdout.write("Header is missing, the message is either malformed or corrupted")
			
		sys.stdout.close()
		
		i = i + 1