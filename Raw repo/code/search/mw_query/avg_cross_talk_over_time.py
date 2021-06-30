import pysolr
import codecs
import sys
import os
import numpy
from tqdm import tqdm
from frame import *

codecs.register_error("strict", codecs.replace_errors)

try:
	os.mkdir("avg_cross_talk_res")
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

avg_home = dict()

avg_other = dict()

div_home = dict()

div_other = dict()

sum_home = 0

sum_other = 0



while year != 2021:

	tmp_home = list()
	tmp_away = list()

	sum = 0
	avg_home[year] = 0
	avg_other[year] = 0



	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"From-address",
	"facet.limit":-1,
	"facet.sort":"count",
	"facet.mincount":1

	}

	adr = [] #list of addresses

	res1 = solr.search("Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)#first get a list of mailing lists


	i = 0
	while i < len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"]):

		adr.append(res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i])

		i = i + 2





	out = open("avg_cross_talk_res" + slash + str(year) + ".txt","w")

	print("\nYear = " + str(year))



	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"Mailing-list",
	"facet.limit":-1,
	"facet.sort":"count",
	"facet.mincount":1

	}




	for x in tqdm(adr):

		try:
			query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + x
			res2 = solr.search(query,**param)

			length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])

			if length < 1:


				query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + fix_adr(x)
				res2 = solr.search(query,**param)

				avg_home[year] = avg_home[year]  + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1]
				sum = sum + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1]

				tmp_home.append(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1])

				i = 3

				while i < len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"]):
					avg_other[year] = avg_other[year] + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i]
					sum = sum + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i]

					tmp_away.append(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i])

					i = i + 2



			else:


				avg_home[year] = avg_home[year]  + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1]
				sum = sum + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1]

				tmp_home.append(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1])

				i = 3

				while i < len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"]):
					avg_other[year] = avg_other[year] + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i]
					sum = sum + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i]

					tmp_away.append(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i])

					i = i + 2





		except:




			query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + fix_adr(x)
			res2 = solr.search(query,**param)

			avg_home[year] = avg_home[year]  + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1]
			sum = sum + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1]

			tmp_home.append(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][1])

			i = 3

			while i < len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"]):
				avg_other[year] = avg_other[year] + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i]
				sum = sum + res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i]

				tmp_away.append(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i])

				i = i + 2


		#print(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])
		#print(len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"]))
		#print(len(adr))



	print("Sum = " + str(sum))
	try:
		print("Sum home = " + str(avg_home[year]))
		sum_home = sum_home + avg_home[year]
		avg_home[year] = avg_home[year]/len(adr)
	except:
		avg_home[year] = 0
		print("Sum home = " + str(avg_home[year]))

	if len(tmp_home) > 1:
		div_home[year] = numpy.std(tmp_home)
	else:
		div_home[year] = 0


	if len(tmp_away) > 1:
		div_other[year] = numpy.std(tmp_away)
	else:
		div_other[year] = 0



	try:
		print("Sum other = " + str(avg_other[year]))
		sum_other = sum_other + avg_other[year]
		avg_other[year] = avg_other[year]/len(adr)
	except:
		avg_other[year] = 0
		print("Sum other = " + str(avg_other[year]))



	print("Avg home = " + str(avg_home[year]))
	print("Avg other = " + str(avg_other[year]))
	year = year + 1




param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}


all_adr = len(solr.search("*:*",**param).raw_response["facet_counts"]["facet_fields"]["From-address"])/2#first get a list of mailing lists

print(sum_home/all_adr)
print(sum_other/all_adr)

div = 0

print("HOME")

tmp = "\\addplot[color=green] coordinates {"

for x in avg_home.keys():
	tmp = tmp + "(" + str(x) + "," + str(avg_home[x]) + ")"


print(tmp + "};\n\n")


tmp = "\\addplot[name path=us_top,color=green!70] coordinates {"

for x in avg_home.keys():
	div = div_home[x]/2
	tmp = tmp + "(" + str(x) + "," + str(avg_home[x] + div) + ")"


print(tmp + "};\n\n")




tmp = "\\addplot[name path=us_down,color=green!70] coordinates {"

for x in avg_home.keys():
	div = div_home[x]/2
	tmp = tmp + "(" + str(x) + "," + str(avg_home[x] - div) + ")"


print(tmp + "};\n\n")

print("\\addplot[green!50,fill opacity=0.5] fill between[of=us_top and us_down];\n\n")












print("\n\n\n\n\n")

print("AWAY")

tmp = "\\addplot[color=green] coordinates {"

for x in avg_other.keys():
	tmp = tmp + "(" + str(x) + "," + str(avg_other[x]) + ")"


print(tmp + "};\n\n")



tmp = "\\addplot[name path=other_top,color=green!70] coordinates {"

for x in avg_other.keys():
	div = div_other[x]/2
	tmp = tmp + "(" + str(x) + "," + str(avg_other[x] + div) + ")"


print(tmp + "};\n\n")


tmp = "\\addplot[name path=other_down,color=green!70] coordinates {"

for x in avg_other.keys():
	div = div_other[x]/2
	tmp = tmp + "(" + str(x) + "," + str(avg_other[x] - div) + ")"


print(tmp + "};\n\n")

print("\\addplot[green!50,fill opacity=0.5] fill between[of=other_top and other_down];\n\n")
