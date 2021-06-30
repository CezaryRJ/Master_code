import pysolr
import codecs
import sys
import os
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



start = 1980
year = start


total = 0

param = {"debugQuery":"off",
"rows" : 0,
"facet":"off", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

year_list = list()
count_list = list()

while year != 2021:
    year_list.append(year)

    res1 = solr.search("Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]",**param)

    count_list.append(res1.raw_response["response"]["numFound"])

    year = year + 1


tmp = ""

i = 0
while i < 41:

    tmp = tmp + "(" + str(year_list[i]) + "," + str(count_list[i]) + ")"

    i = i + 1

print(tmp)
