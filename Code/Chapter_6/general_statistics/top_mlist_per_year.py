from frame import *
import sys




solr = connect_to_solr(sys.argv[1])

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":1,
"facet.sort":"count",
"facet.mincount":1

}

slash = get_slash()



start = 1990

year = start


top_per_year = dict()

while year < 2021:

	#print(str(year) + "-01-01T00:00:00Z")
    query = "Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR]"

    res = solr.search(query,**param)

    top_per_year[year] = res.raw_response["facet_counts"]["facet_fields"]["Mailing-list"]

    year = year + 1


print("\\begin{center}")
print(" \\begin{tabular}{|c | c | c|} ")
print(" \hline")
print(" Year & Mailing-list & Count \\\\ [0.5ex] ")
print(" \hline\hline")


for x in top_per_year:

    print(str(x) + " & " + str(top_per_year[x][0]) + " & " + str(top_per_year[x][1]) + "\\\\")
    print("\hline")



print("\hline")

print("\end{tabular}")
print("\end{center}")
