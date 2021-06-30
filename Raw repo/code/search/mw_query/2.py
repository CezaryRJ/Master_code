import pysolr
import codecs
import sys
from frame import *
from tqdm import tqdm

codecs.register_error("strict", codecs.replace_errors)

try:
	print("\nUsing core " + sys.argv[1] + "\n")
except:
	print("No core name provided")
	exit()

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}


res1 = solr.search("*:*",**param)#first get a list of mailing lists
i = 0

adr = [] #list of addresses

while i < len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"]):

	adr.append(res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i])

	i = i + 2



param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}



sum = 0
removed = 0
remove_list = []
for x in tqdm(adr):
	length = 0

	try:

		res2 = solr.search("From-address:" + x ,**param) #this may fail as some characters are not allowes in the query field
		length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2

		if length == 0:
			res2 = solr.search("From-address:" + fix_adr(x) ,**param) #this may fail as some characters are not allowes in the query field
			length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2
			if length == 0:
				print(x)
				print(fix_adr(x))
				print("_")
				exit()

		sum = sum + length

	except:

		res2 = solr.search("From-address:" + fix_adr(x) ,**param) #this may fail as some characters are not allowes in the query field

		length = len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2

		if length == 0:
			print(x)
			print(fix_adr(x))
			print("_")
			exit()

		sum = sum + length


		#removed = removed + 1
		#remove_list.append(x)
		#print("\nRemoved " + x + "\n")

	#print(len(res2.raw_response["facet_counts"]["facet_fields"]["Mailing-list"])/2)



print("Adr count = " + str(len(adr)))
print("Removed " + str(removed))
print("Sum " + str(sum))

print("Avarage = " + str(sum/(len(adr)-removed)))


out = open("2_res.txt","w")

out.write("Adr count = " + str(len(adr)) + "\n")
out.write("Removed " + str(removed) + "\n")
out.write("Sum " + str(sum) + "\n")
out.write("Avarage = " + str(sum/(len(adr)-removed)) + "\n")

out.close()

out = open("2_removed.txt","w")
for x in remove_list:
	out.write(str(x) + "\n")

out.close()
