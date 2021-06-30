from frame import *
import sys
from tqdm import tqdm
import numpy



slash = get_slash()

blacklist = open("blacklist.txt","r").readlines()

wg = open("match.txt","r").readlines()

solr_rfc = connect_to_solr("rfc")

solr = connect_to_solr("ietf-archive-final-v2")

results_before = dict()
results_after = dict()



start = 1990
year = start


for x in tqdm(wg):

    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"date",
    "facet.limit":-1,
    "facet.sort":"index",
    "facet.mincount":1

    }


    #print(x)
    res = solr_rfc.search("wg:"+ x[:-1],**param)

    dates = list()#dates of all rfcs from a working group

    i = 0



    while i < len(res.raw_response["facet_counts"]["facet_fields"]["date"]):
        dates.append(res.raw_response["facet_counts"]["facet_fields"]["date"][i])
        i = i + 2

#"Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]"


    param = {"debugQuery":"off",
    "rows" : 0
     }


    for y in dates:

        i = 1
        while i < 7: #before publication

        #    print("Mailing-list:"+ x[:-1] + " AND Date:[" + y +"-" + str(i) + "MONTH"+ " TO " + y + "]")

            res = solr.search("Mailing-list:"+ x[:-1] + " AND Date:[" + y +"-" + str(i) + "MONTH"+ " TO " + y +"-" + str(i-1) + "MONTH"+ "]",**param)

            try:
                results_before[i].append(res.raw_response["response"]["numFound"])

            except:
                results_before[i] = list()
                results_before[i].append(res.raw_response["response"]["numFound"])

            i = i + 1

            #print(res.raw_response)



        i = 1
        while i < 8: #before publication

            #print("Mailing-list:"+ x[:-1] + " AND Date:[" + y +"+" + str(i) + "MONTH"+ " TO " + y +"-" + str(i-1) + "MONTH"+ "]")

            res = solr.search("Mailing-list:"+ x[:-1] + " AND Date:[" + y +"+" + str(i-1) + "MONTH"+ " TO " + y +"+" + str(i) + "MONTH"+ "]",**param)

            try:
                results_after[i-1].append(res.raw_response["response"]["numFound"])

            except:
                results_after[i-1] = list()
                results_after[i-1].append(res.raw_response["response"]["numFound"])

            i = i + 1


print("\n\nmean\n")
#print(results_before)

print("\n\n\\addplot[color=red] coordinates {")

for x in list(reversed(sorted(results_before.keys()))):
    print("(-" + str(x) + "," + str(numpy.mean(results_before[x])) +")")

#print(results_after)
for x in results_after:
    print("(+" + str(x) + "," + str(numpy.mean(results_after[x])) + ")")

print("\n\n};")



print("\\addplot[name path=us_top,color=blue!70] coordinates {")

for x in list(reversed(sorted(results_before.keys()))):
    print("(-" + str(x) + "," + str(numpy.mean(results_before[x]) + (numpy.std(results_before[x])/2)) +")")

#print(results_after)
for x in results_after:
    print("(+" + str(x) + "," + str(numpy.mean(results_after[x]) + (numpy.std(results_after[x])/2)) +")")

print("\n\n};")




print("\\addplot[name path=us_down,color=blue!70] coordinates {")

for x in list(reversed(sorted(results_before.keys()))):
    print("(-" + str(x) + "," + str(numpy.mean(results_before[x]) - (numpy.std(results_before[x])/2)) +")")

#print(results_after)
for x in results_after:
    print("(+" + str(x) + "," + str(numpy.mean(results_after[x]) - (numpy.std(results_after[x])/2)) +")")

print("\n\n};")
