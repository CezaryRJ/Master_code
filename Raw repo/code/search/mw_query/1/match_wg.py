import pysolr
import codecs
import sys
import os
import numpy
from frame import *
from tqdm import tqdm


codecs.register_error("strict", codecs.replace_errors)



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

file = open("wg.txt","r").readlines()





param = {"debugQuery":"off",
"rows" : 0
}

match_list = list()
mismatch_list = list()

yes_match = 0
no_match = 0



for x in file:
	res = solr.search("Mailing-list:" + x[:-1],**param)

	if res.raw_response["response"]["numFound"] > 0:
		match_list.append(x[:-1])
		#print(x[:-1])
		yes_match = yes_match + 1
	else:
		#print(x[:-1])
		mismatch_list.append(x[:-1])
		no_match = no_match + 1






print(yes_match)

print(no_match)

print(len(file))

out = open("match.txt","w")

for x in match_list:
	out.write(str(x) + "\n")

out.close()


out = open("mismatch.txt","w")

for x in mismatch_list:
	out.write(str(x) + "\n")

out.close()
