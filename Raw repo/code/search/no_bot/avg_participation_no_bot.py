import pysolr
import codecs
import sys
import os
from frame import *
from tqdm import tqdm

codecs.register_error("strict", codecs.replace_errors)

folder_name = "avg_participation_res"

try:
	os.mkdir(folder_name)
except:
	pass


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


blacklist = open("blacklist.txt","r").readlines()



param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

res1 = solr.search("*:*",**param)#first get a list of mailing lists

adr = dict() #list of addresses


i = 0
while i < len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"]):

	adr[res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i]] = 0

	i = i + 2





param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

results = dict()

sum = 0

removed = []

for x in tqdm(adr):


	try:

		res2 = solr.search("From-address:" + x,**param)

		length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2


		if length < 1:
			res2 = solr.search("From-address:" + fix_adr(x),**param)
			length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
			if length < 1: #failsafe
				print(x)
				exit()

		sum = sum + length

		results[x] = length

	except:

		res2 = solr.search("From-address:" + fix_adr(x),**param)
		length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
		if length < 1: #failsafe
			print(x)
			exit()

		sum = sum + length

		results[x] = length



try:
	results.pop("Null")
except KeyError:
	pass


ignore_case_list = dict()

for x in results:

	try:

		ignore_case_list[x.lower()] = ignore_case_list[x.lower()] + results[x]

	except KeyError :

		ignore_case_list[x.lower()] = results[x]


for x in blacklist:
	try:
		results.pop(x[:-1])
		print("Removed " + str(x))
	except KeyError:
		pass

count = dict()

for x in results:
	try:
		count[results[x]] = count[results[x]] + 1

	except KeyError:
		count[results[x]] = 1

count = dict(sorted(count.items(), key=lambda item: item[1]))




sorted_keys = sorted(count.keys())

sum = 0

for x in sorted_keys:
	print("(" + str(x) + "," + str(count[x]) + ")",end = "")
	sum = sum + count[x]

#x , y
x_line = 0
print("\n\n\n")
for x in sorted_keys:
	x_line = x_line + count[x]
	print("(" +  str(x) + "," + str(x_line/sum) + ")",end="")
