import pysolr
import codecs
import sys
import os
from tqdm import tqdm
from frame import *

codecs.register_error("strict", codecs.replace_errors)

try:
	os.mkdir("avg_participation_over_time_res")
except:
	pass


slash = "\\"

if sys.platform == "win32":
	print("\n\nRunning on Windows\n")
else:
	slash = "/"
	print("\n\nRunning on Unix\n")

xtick = []
ytick = []

try:
	print("\nUsing core " + sys.argv[1] + "\n")
except:
	print("No core name provided")
	exit()

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])


start = 1990
year = start


part = dict()
ppl = dict()



total = 0

while year != 2021:

	print("\n" + str(year))

	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"From-address",
	"facet.limit":-1,
	"facet.sort":"count",
	"facet.mincount":1

	}



	res1 = solr.search("Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)

	adr = [] #list of addresses


	i = 0
	while i < len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"]):

		adr.append(res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i])

		i = i + 2

	print("Adr count = " + str(len(adr)))

	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"Mailing-list",
	"facet.limit":-1,
	"facet.sort":"count",
	"facet.mincount":1

	}

	for x in tqdm(adr):

		#print(str(i) + " / " + str(len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"])))

		try:

			res2 = solr.search("From-address:" + x + " AND Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)

			length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2

			if length < 1:
				res2 = solr.search("From-address:" + fix_adr(x) + " AND Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)
				length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
				if length < 1: #failsafe
					print(x)
					exit()



			try:
				part[length] = part[length] + 1
				ppl[length].append(x)
			except:
				part[length] = 1
				ppl[length] = list()
				ppl[length].append(x)



		except:

			res2 = solr.search("From-address:" + fix_adr(x) + " AND Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)
			length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
			if length < 1: #failsafe
				print(x)
				exit()


			try:
				part[length] = part[length] + 1
				ppl[length].append(x)
			except:
				part[length] = 1
				ppl[length] = list()
				ppl[length].append(x)




	out = open("avg_participation_over_time_res" + slash + str(year) + "_res" + ".txt","w")

	sorted_keys = sorted(part.keys())

	out.write("Sum = " + str(len(adr)) + "\n\n")

	for x in sorted_keys:
		out.write(str(x) + "  " + str(part[x]) + "\n")

	out.close()



	out = open("avg_participation_over_time_res" + slash + str(year) + "_ppl" + ".txt","w")

	for x in sorted_keys:
		out.write(str(x) + "\n")
		for y in ppl[x]:
			out.write(y + "\n")

		out.write("\n")

	out.close()






	year = year + 1
