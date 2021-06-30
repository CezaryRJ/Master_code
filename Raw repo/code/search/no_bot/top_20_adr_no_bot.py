from frame import *
import sys





solr = connect_to_solr(sys.argv[1])

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":50,
"facet.sort":"count",
"facet.mincount":1

}

slash = get_slash()

res1 = solr.search("*:*",**param)

i = 0

results = dict()

facet_list = res1.raw_response["facet_counts"]["facet_fields"]["From-address"]

while i < len(facet_list):

    try:
        results[(facet_list[i]).lower()] = results[(facet_list[i]).lower()] + (facet_list[i+1])

    except:

        results[(facet_list[i]).lower()] = facet_list[i+1]

    i = i + 2

try:
    results.pop("null")
except KeyError:
    pass

blacklist = open("blacklist.txt","r").readline()

for x in blacklist:
    try:
        results.pop(x[:-1])
    except KeyError:
        pass

print("\\begin{center}")
print(" \\begin{tabular}{|c | c | c|} ")
print(" \hline")
print("Ranking & address & Value \\\\ [0.5ex] ")
print(" \hline\hline")

blacklist = open("blacklist.txt","r").readlines()

for x in blacklist:
    try:
        results.pop(x[:-1])
    except:
        pass

Ranking = 1
for x in results:
    print(" " + str(Ranking) + " & " + str(x).replace("_","\_") + " & " + str(results[x]) + "\\\\")
    print("  \hline")

    Ranking = Ranking + 1

    if Ranking == 21:
        break

print("\end{tabular}")
print("\end{center}")
