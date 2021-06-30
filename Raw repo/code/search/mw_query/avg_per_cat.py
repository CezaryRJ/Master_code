import pysolr
import codecs
import sys
import os
from frame import *
from tqdm import tqdm

codecs.register_error("strict", codecs.replace_errors)


folder_name = "avg_per_cat_res"

try:
	os.mkdir(folder_name)
except:
	pass


param = {"debugQuery":"off",
"rows" : 0
}

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])





a = open("avg_participation_res/res_ppl.txt","r").readlines()

cat = dict()

i = 0
y = 1

while i < 50:
	cat[i] = []

	while a[y] != "\n":
		cat[i].append(a[y].strip())
		y = y + 1

	i = i + 1
	y = y + 2


res = []

for x in cat.keys():
	print(x)
	res.append(x)
	for y in tqdm(cat[x]):

		try:

			found = solr.search("From-address:" + y,**param).raw_response["response"]["numFound"]

			if found == 0:

				found = solr.search("From-address:" + fix_adr(y),**param).raw_response["response"]["numFound"]
				res[x] = res[x] + found

			else:

				res[x] = res[x] + found

		except:

			found = solr.search("From-address:" + fix_adr(y),**param).raw_response["response"]["numFound"]

			if found == 0:

				found = solr.search("From-address:" + fix_adr(y),**param).raw_response["response"]["numFound"]
				res[x] = res[x] + found

			else:

				res[x] = res[x] + found



	res[x] = res[x]/len(cat[x])
	print(res[x])
tmp = ""

i = 0
while i < len(res):
	tmp = tmp + ("(" + str(i) +"," + str(res[i]) + ")")
	i = i + 1


print(tmp)
