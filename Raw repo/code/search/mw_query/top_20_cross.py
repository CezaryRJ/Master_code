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

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}



top_20 = []

try:
	print("\nUsing core " + sys.argv[1] + "\n")
except:
	print("No core name provided")
	exit()

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}
