import pysolr
import os
from sapi import *
import codecs
import sys

latex_table = list()
latex_table.append("\\begin{center}")
latex_table.append(" \\begin{tabular}{|c | c|} ")
latex_table.append(" \hline")
latex_table.append(" Category & Value \\\\ [0.5ex] ")
latex_table.append(" \hline\hline")


codecs.register_error("strict", codecs.replace_errors)

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

print("\nUsing core " + sys.argv[1] + "\n")

param = {"debugQuery":"off",
"rows" : 0
}


query = "From:Null AND Date:\"1900-01-01T01:00:00Z\" AND (To:Null AND Cc:Null AND Bcc:Null)"

res1 = solr.search(query,**param)#first get a list of mailing lists

docs = res1.raw_response["response"]["numFound"]

print("From + Date + Dest = " + str(docs))

latex_table.append("From + Date + Dest & " + str(docs) + "\\\\")
latex_table.append("\hline")





query = "From:Null AND Date:\"1900-01-01T01:00:00Z\" AND NOT (To:Null AND Cc:Null AND Bcc:Null)"

res1 = solr.search(query,**param)#first get a list of mailing lists

docs = res1.raw_response["response"]["numFound"]

print("From + Date = " + str(docs))

latex_table.append("From + Date & " + str(docs) + "\\\\")
latex_table.append("\hline")






query = "From:Null AND NOT Date:\"1900-01-01T01:00:00Z\" AND (To:Null AND Cc:Null AND Bcc:Null)"

res1 = solr.search(query,**param)#first get a list of mailing lists

docs = res1.raw_response["response"]["numFound"]

print("From + Dest = " + str(docs))

latex_table.append("From + Dest & " + str(docs) + "\\\\")
latex_table.append("\hline")






query = "NOT From:Null AND Date:\"1900-01-01T01:00:00Z\" AND (To:Null AND Cc:Null AND Bcc:Null)"

res1 = solr.search(query,**param)#first get a list of mailing lists

docs = res1.raw_response["response"]["numFound"]

print("Date + Dest = " + str(docs))

latex_table.append("Date + Dest & " + str(docs) + "\\\\")
latex_table.append("\hline")





query = "From:Null AND NOT Date:\"1900-01-01T01:00:00Z\" AND NOT (To:Null AND Cc:Null AND Bcc:Null)"

res1 = solr.search(query,**param)#first get a list of mailing lists

docs = res1.raw_response["response"]["numFound"]

print("From = " + str(docs))

latex_table.append("From & " + str(docs) + "\\\\")
latex_table.append("\hline")






query = "NOT From:Null AND Date:\"1900-01-01T01:00:00Z\" AND NOT (To:Null AND Cc:Null AND Bcc:Null)"

res1 = solr.search(query,**param)#first get a list of mailing lists

docs = res1.raw_response["response"]["numFound"]

print("Date = " + str(docs))

latex_table.append("Date & " + str(docs) + "\\\\")
latex_table.append("\hline")






query = "NOT From:Null AND NOT Date:\"1900-01-01T01:00:00Z\" AND (To:Null AND Cc:Null AND Bcc:Null)"

res1 = solr.search(query,**param)#first get a list of mailing lists

docs = res1.raw_response["response"]["numFound"]

print("Dest = " + str(docs))

latex_table.append("Dest & " + str(docs) + "\\\\")
latex_table.append("\hline")




query = "From:Null OR Date:\"1900-01-01T01:00:00Z\" OR (To:Null AND Cc:Null AND Bcc:Null)"

res1 = solr.search(query,**param)#first get a list of mailing lists

docs = res1.raw_response["response"]["numFound"]

print("ALL = " + str(docs))


latex_table.append("ALL & " + str(docs) + "\\\\")
latex_table.append("\hline")

latex_table.append("\end{tabular}")
latex_table.append("\end{center}")

for x in latex_table:
    print(x)
