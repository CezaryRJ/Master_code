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


try:
	print("\nUsing core " + sys.argv[1] + "\n")
except:
	print("No core name provided")
	exit()

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

blacklist = open("blacklist.txt","r").readlines()

start = 1990
year = start


#0 is home
#1 is away

res_home = dict()
res_away = dict()

div_home = dict()
div_away = dict()


while year != 2021:

	print(year)

	param = {"debugQuery":"off",
	"rows" : 0,
	"facet":"on", #if this is set to "off" then no facet will be returned
	"facet.field":"From-address",
	"facet.limit":-1,
	"facet.sort":"count",
	"facet.mincount":1

	}

	adr = dict() #list of addresses

	res1 = solr.search("Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)#first get a list of mailing lists


	i = 0
	while i < len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"]):

		adr[res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i]] = list()

		i = i + 2

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

			if length < 1:#if no results ,try "fixing" the address and try again

				query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + fix_adr(x)
				res2 = solr.search(query,**param)

				fct_list = facet_to_list(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])

				adr[x].append(fct_list[0]) #home count
				adr[x].append(fct_list[1:]) #away count

			else:

				fct_list = facet_to_list(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])

				adr[x].append(fct_list[0]) #home count
				adr[x].append(fct_list[1:]) #away count



		except:#if exception ,try "fixing" the address and try again

			query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + fix_adr(x)
			res2 = solr.search(query,**param)

			fct_list = facet_to_list(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])

			adr[x].append(fct_list[0]) #home count
			adr[x].append(fct_list[1:]) #away count



	for x in blacklist:
		try:
			adr.pop(x[:-1])
			#print("Removed " + x[:-1])
		except KeyError:
			pass



	tmp_home = list()
	tmp_away = list()
	for x in adr:
		tmp_home.append(adr[x][0])
		if len(adr[x][1]) > 0:
			for y in adr[x][1]:
				tmp_away.append(int(y))
		else:
			tmp_away.append(0)


	res_home[year] = numpy.average(tmp_home)
	res_away[year] = numpy.average(tmp_away)

	print("AVG HOME = " + str(res_home[year]))
	print("AVG AWAY = " + str(res_away[year]))


	div_home[year] = numpy.std(tmp_home)
	div_away[year] = numpy.std(tmp_away)

	print("DIV HOME = " + str(div_home[year]))
	print("DIV AWAY = " + str(div_away[year]))


	year = year + 1

print("\n\n\nHOME")




print("\\addplot[color=green] coordinates {")

for x in res_home:
	print("(" + str(x) + "," + str(res_home[x]) + ")",end="")

print("};\n\n")



print("\\addplot[name path=us_top,color=green!70] coordinates {")

for x in res_home:
	print("(" + str(x) + "," + str(res_home[x] + div_home[x]/2) + ")",end="")

print("};\n\n")

print("\\addplot[name path=us_down,color=green!70] coordinates {")

for x in res_home:
	print("(" + str(x) + "," + str(res_home[x] - div_home[x]/2) + ")",end="")

print("};\n\n")


print("\\addplot[green!50,fill opacity=0.5] fill between[of=us_top and us_down];\n\n")





print("\n\n\nAWAY")



print("\\addplot[color=green] coordinates {")

for x in res_away:
	print("(" + str(x) + "," + str(res_away[x]) + ")",end="")

print("};\n\n")

print("\\addplot[name path=div_top,color=green!70] coordinates {")
for x in res_away:
	print("(" + str(x) + "," + str(res_away[x] + div_away[x]/2) + ")",end="")

print("};\n\n")

print("\\addplot[name path=div_down,color=green!70] coordinates {")
for x in res_away:
	print("(" + str(x) + "," + str(res_away[x] - div_away[x]/2) + ")",end="")

print("};\n\n")

print("\\addplot[green!50,fill opacity=0.5] fill between[of=div_top and div_down];\n\n")
