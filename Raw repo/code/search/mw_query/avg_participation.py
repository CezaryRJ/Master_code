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

adr = [] #list of addresses


i = 0
while i < len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"]):

	adr.append(res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i])

	i = i + 2





param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}


part = dict()
ppl = dict()

sum = 0

removed = []

for x in tqdm(adr):

	#print(str(i) + " / " + str(len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"])))
	#print(len(part))
	#print(len(ppl))
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

		try:
			part[length] = part[length] + 1
			ppl[length].append(x)
		except:
			part[length] = 1
			ppl[length] = list()
			ppl[length].append(x)

	except:

		res2 = solr.search("From-address:" + fix_adr(x),**param)
		length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
		if length < 1: #failsafe
			print(x)
			exit()

		sum = sum + length

		try:
			part[length] = part[length] + 1
			ppl[length].append(x)
		except:
			part[length] = 1
			ppl[length] = list()
			ppl[length].append(x)







sorted_keys = sorted(part.keys())


for x in sorted_keys:
	print("(" + str(x) + "," + str(part[x]) + ")",end="")




out = open(folder_name + slash + "res.txt","w")

out.write("Sum = " + str(sum) + "\n\n")

for x in sorted_keys:
	out.write(str(x) + "  " + str(part[x]) + "\n")

out.close()



out = open(folder_name + slash + "res_ppl.txt","w")

for x in sorted_keys:
	out.write(str(x) + "\n")
	for y in ppl[x]:
		out.write(y + "\n")

	out.write("\n")

out.close()



out = open(folder_name + slash + "removed.txt","w")

for x in removed:
	out.write(x + "\n")

out.close()
