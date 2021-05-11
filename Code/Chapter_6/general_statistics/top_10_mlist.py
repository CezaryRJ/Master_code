from frame import *
import sys


latex_table = list()
latex_table.append("\\begin{center}")
latex_table.append(" \\begin{tabular}{|c | c | c|} ")
latex_table.append(" \hline")
latex_table.append("Ranking & address & Value \\\\ [0.5ex] ")
latex_table.append(" \hline\hline")



solr = connect_to_solr(sys.argv[1])

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":10,
"facet.sort":"count",
"facet.mincount":1

}

slash = get_slash()

res1 = solr.search("*:*",**param)

i = 0
ranking = 1
while i < 20:


    print(str(res1.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i]) + "  ",end='')
    print(res1.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i+1])


    latex_table.append(str(ranking) + " & " + res1.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i].replace("_","\_") + " & "  +  str(res1.raw_response["facet_counts"]["facet_fields"]["Mailing-list"][i+1]) +  "\\\\")
    latex_table.append("\hline")

    ranking = ranking + 1

    i = i + 2




latex_table.append("\end{tabular}")
latex_table.append("\end{center}")


for x in latex_table:
    print(x)
