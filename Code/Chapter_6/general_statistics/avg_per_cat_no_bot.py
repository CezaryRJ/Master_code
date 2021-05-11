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

removed = []

for x in tqdm(adr):


	try:

		res2 = solr.search("From-address:" + x,**param)

		length = int(len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2)


		if length < 1:
			res2 = solr.search("From-address:" + fix_adr(x),**param)
			length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
			if length < 1: #failsafe
				print(x)
				exit()


		try:
			results[length].append(x)
		except:
			results[length] = list()
			results[length].append(x)

	except:

		res2 = solr.search("From-address:" + fix_adr(x),**param)
		length = int(len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2)
		if length < 1: #failsafe
			print(x)
			exit()

		try:
			results[length].append(x)
		except:
			results[length] = list()
			results[length].append(x)


blacklist = open("blacklist.txt","r").readlines()

#remove blacklisted
for x in blacklist:
	for y in results:
		try:
			results[y].remove(x[:-1])
			print("Removed " + str(x[:-1]) + " from cat " + str(y))
		except ValueError:
			pass



param = {"debugQuery":"off",
"rows" : 0
}


sorted_keys = sorted(results.keys())

res = dict()

i = 0

for x in sorted_keys:
	print(x)
	res[x] = 0
	for y in tqdm(results[x]):

		try:

			found = solr.search("From-address:" + y,**param).raw_response["response"]["numFound"]

			if found == 0:

				found = solr.search("From-address:" + fix_adr(y),**param).raw_response["response"]["numFound"]
				res[x] = res[x] + found

			else:

				res[x] = res[x] + found

		except:

			found = solr.search("From-address:" + fix_adr(y),**param).raw_response["response"]["numFound"]

			if found == 0:

				found = solr.search("From-address:" + fix_adr(y),**param).raw_response["response"]["numFound"]
				res[x] = res[x] + found

			else:

				res[x] = res[x] + found


	if len(results[x]) == 0:
		res[x] = 0
	else:
		res[x] = res[x]/len(results[x])

	print(str(x) + "  " +  str(res[x]))

	if i == 50:
		break

	i = i + 1




i = 0
for x in res:
	print("(" + str(x) +"," + str(res[x]) + ")",end="")

	if i == 50:
		break

	i = i + 1

print("\n")
