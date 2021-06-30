import pysolr
import codecs
import sys
import os
import numpy
from tqdm import tqdm
from frame import *

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



total = 0

remove_list = []

year_list = []

avg_list = []

div_list = list()

tmp_list = list()

while year != 2021:

	tmp_list = list()

	year_list.append(year)

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





	out = open("avg_over_time_res" + slash + str(year) + ".txt","w")

	print("\nYear = " + str(year))


	sum = 0
	removed = 0





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

			length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2

			if length < 1:
				query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + fix_adr(x)
				res2 = solr.search(query,**param)
				length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
				if length < 1:
					print(x)
					print(fix_adr(x))
					exit()

			sum = sum + length

			tmp_list.append(length)

		except:

			query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND From-address:" + fix_adr(x)
			res2 = solr.search(query,**param)
			length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
			if length < 1:
				print(x)
				print(fix_adr(x))
				exit()

			sum = sum + length

			tmp_list.append(length)

			#print("\nRemoved " + x + "\n")


	print("Year = " + str(year))
	print("Adr count = " + str(len(adr)))
	print("Removed " + str(removed))
	print("Sum " + str(sum))

	#print(tmp_list)
	if len(tmp_list) > 0:

		try:

			print("STD DIV = " + str(numpy.std(tmp_list)))
			div_list.append(numpy.std(tmp_list))

		except:
			print("STD DIV = " + str(0))
			div_list.append(0)
	else:
		print("STD DIV = " + str(0))
		div_list.append(0)



	try:
		print("Avarage = " + str(sum/(len(adr)-removed)))
	except:
		print("Avarage = 0")


	#output file
	out.write("Year = " + str(year) + "\n")
	out.write("Adr count = " + str(len(adr)) + "\n")
	out.write("Removed " + str(removed) + "\n")
	out.write("Sum " + str(sum) + "\n")

	try:
		out.write("Avarage = " + str(sum/(len(adr)-removed)) + "\n")
		xtick.append(sum/(len(adr)-removed))
		avg_list.append(sum/(len(adr)-removed))
	except:
		out.write("Avarage = 0\n")
		xtick.append(0)
		avg_list.append(0)

	out.close()

	ytick.append(year)


	year = year + 1


out = open("avg_over_time_res" + slash + "removed.txt","w")

for x in remove_list:
	out.write(x + "\n")

out.close()

print("Total = " + str(total))


out = open("avg_over_time_res" + slash + "latex_input.txt","w")

for x in ytick:
	out.write(str(x) + ",")

out.write("\n")

for x in xtick:
	out.write(str(x) + ",")


out.close()

tmp = "\\addplot[color=green] coordinates {"

i = 0

while i < 31:

	tmp = tmp + "(" + str(year_list[i]) + "," + str(avg_list[i]) + ")"
	i = i + 1

print(tmp + "};\n\n")




tmp = "\\addplot[name path=us_top,color=green!70] coordinates {"

i = 0


while i < 31:

	div = div_list[i]/2

	tmp = tmp + "(" + str(year_list[i]) + "," + str(avg_list[i] + div) + ")"
	i = i + 1



print(tmp + "};\n\n")




tmp = "\\addplot[name path=us_down,color=green!70] coordinates {"

i = 0


while i < 31:

	div = div_list[i]/2

	tmp = tmp + "(" + str(year_list[i]) + "," + str(avg_list[i] - div) + ")"
	i = i + 1


print(tmp + "};\n\n")

print("\\addplot[green!50,fill opacity=0.5] fill between[of=us_top and us_down];\n\n")





print("\n\n\n\n\n\n")

i = 0

print("\\begin{center}")
print(" \\begin{tabular}{|c | c|} ")
print(" \hline")
print(" Year & Standard deviation \\\\ [0.5ex] ")
print(" \hline\hline")


while i < 31:

	print("  " + str(year_list[i]) + " & " + str(div_list[i]) + "\\\\")
	print("  \hline")
	i = i + 1

print("\hline")

print("\end{tabular}")
print("\end{center}")
