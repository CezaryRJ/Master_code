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


tmp = ""

print("HOME")

tmp_list = list()

for x in avg_home.keys():
	tmp = tmp + "(" + str(x) + "," + str(avg_home[x]) + ")"
	tmp_list.append(avg_home[x])

print(tmp)

std_dev = numpy.std(tmp_list)

print("Standard deviation for the home plot = " + str(numpy.std(tmp_list)))

print("\n\n\n\n")
print("\\begin{center}")
print(" \\begin{tabular}{|c | c|} ")
print(" \hline")
print(" Year & Standard deviation \\\\ [0.5ex] ")
print(" \hline\hline")

for x in div_home:
	print("  " + str(x) + " & " + str(div_home[x]) + "\\\\")
	print("  \hline")

print("\hline")

print("\end{tabular}")
print("\end{center}")

print("\n\n\n\n\n")

tmp = ""
print("AWAY")

tmp_list = list()


for x in avg_other.keys():
	tmp = tmp + "(" + str(x) + "," + str(avg_other[x]) + ")"
	tmp_list.append(avg_home[x])

print(tmp)

print("\n\n\n\n")
print("\\begin{center}")
print(" \\begin{tabular}{|c | c|} ")
print(" \hline")
print(" Year & Standard deviation \\\\ [0.5ex] ")
print(" \hline\hline")

for x in div_other:
	print("  " + str(x) + " & " + str(div_other[x]) + "\\\\")
	print("  \hline")

print("\hline")

print("\end{tabular}")
print("\end{center}")
