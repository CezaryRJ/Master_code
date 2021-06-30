import pysolr
import codecs
import sys
import os
import numpy
from frame import *
from tqdm import tqdm


codecs.register_error("strict", codecs.replace_errors)

try:
	os.mkdir("avg_over_time_res")
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

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])



start = 1990
year = start


sum_plot = dict()
human_plot = dict()
bot_plot = dict()


blacklist = open("blacklist.txt","r").readlines()





while year != 2021:

	print("\n\n" + str(year))

	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"From-address",
	"facet.limit":-1,
	"facet.sort":"count",
	"facet.mincount":1
	}


	#first get addresses and stats
	stats = dict()

	res = solr.search("Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)#first get a list of mailing lists

	i = 0
	while i < len(res.raw_response["facet_counts"]["facet_fields"]["From-address"]):

		try:
			stats[res.raw_response["facet_counts"]["facet_fields"]["From-address"][i]] = 0

		except KeyError:
			pass

		i = i + 2



	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"Mailing-list",
	"facet.limit":-1,
	"facet.sort":"count",
	"facet.mincount":1

	}



	for x in tqdm(stats):

		try:

			query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + x
			res2 = solr.search(query,**param)


			if len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"]) < 1:
				query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + fix_adr(x)
				res2 = solr.search(query,**param)


				if len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"]) < 1:
					print(x)
					print(fix_adr(x))
					exit()


			stats[x] = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2

		except:

			query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + fix_adr(x)
			res2 = solr.search(query,**param)



			if len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"]) < 1:
				print(x)
				print(fix_adr(x))
				exit()


			stats[x] = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2



	try:
		stats.pop("Null")
	except KeyError:
		pass

	# put everything to lower case
	ignore_case_list = dict()

	for x in stats:

		try:

			ignore_case_list[x.lower()] = ignore_case_list[x.lower()] + stats[x]

		except KeyError :

			ignore_case_list[x.lower()] = stats[x]


	sum_plot[year] = list()

	sum_plot[year].append(numpy.average(list(ignore_case_list.values())))
	sum_plot[year].append(numpy.std(list(ignore_case_list.values())))
	print("Sum plot avg = " + str(sum_plot[year][0]))
	print("Sum plot std = " + str(sum_plot[year][1]))


	bot_list = dict()


	for x in blacklist: #remove blaclisted items

		try:
			bot_list[x[:-1]] = ignore_case_list.pop(x[:-1])#remove newline
			#print("BOT FOUND = " + str(x))
		except KeyError :
			pass

	human_plot[year] = list()
	human_plot[year].append(numpy.average(list(ignore_case_list.values())))
	human_plot[year].append(numpy.std(list(ignore_case_list.values())))
	print("Human plot avg = " + str(human_plot[year][0]))
	print("Human plot std = " + str(human_plot[year][1]))


	bot_plot[year] = list()
	if len(bot_list) > 0:
		bot_plot[year].append(numpy.average(list(bot_list.values())))
		bot_plot[year].append(numpy.std(list(bot_list.values())))
	else:
		bot_plot[year].append(0)
		bot_plot[year].append(0)

	print("Bot plot avg = " + str(bot_plot[year][0]))
	print("Bot plot std = " + str(bot_plot[year][1]))


	year = year + 1
			#print("\nRemoved " + x + "\n")


print("\n\n\nSum plot")

print("\\addplot[color=green] coordinates {")

for x in sum_plot:
	print("(" + str(x) + "," + str(sum_plot[x][0]) + ")",end="")

print("};")




print("\n\n\n\n\nHuman")

for x in human_plot:
	print("(" + str(x) + "," + str(human_plot[x][0]) + ")",end="")
















print("\\begin{center}")
print(" \\begin{tabular}{|c | c|} ")
print(" \hline")
print(" Year & Standard deviation \\\\ [0.5ex] ")
print(" \hline\hline")


for x in human_plot:
		print("  " + str(x) + " & " + str(human_plot[x][1]) + "\\\\")
		print("  \hline")


print("\hline")

print("\end{tabular}")
print("\end{center}")






print("\n\n\n\n\nBot")

for x in bot_plot:
	print("(" + str(x) + "," + str(bot_plot[x][0]) + ")",end="")
