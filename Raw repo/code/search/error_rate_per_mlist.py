import pysolr
import os
from sapi import *
import codecs
import sys






codecs.register_error("strict", codecs.replace_errors)

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1])

print("\nUsing core " + sys.argv[1] + "\n")

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

#first get list of all mailing lists
query = "*:*"

tmp = solr.search(query,**param).raw_response["facet_counts"]["facet_fields"]["Mailing-list"]#first get a list of mailing lists

m_list = []

i = 0

while i < len(tmp):
    m_list.append(tmp[i])
    i = i + 2



param = {"debugQuery":"off",
"rows" : 0
}



for x in m_list:

    latex_table = list()
    latex_table.append("\\begin{center}")
    latex_table.append(" \\begin{tabular}{|c | c|} ")
    latex_table.append(" \hline")
    latex_table.append(" Category & Value \\\\ [0.5ex] ")
    latex_table.append(" \hline\hline")


    query = "(From:Null OR Date:\"1900-01-01T01:00:00Z\" OR (To:Null AND Cc:Null AND Bcc:Null))" + " AND Mailing-list:" + x

    res1 = solr.search(query,**param)#first get a list of mailing lists

    docs = res1.raw_response["response"]["numFound"]


    if docs > 0:

        print("\nStats for mailing list " + x)

        print("\nALL = " + str(docs))

        latex_table.append("All & " + str(docs) + "\\\\")
        latex_table.append("\hline")



        query = "From:Null AND Date:\"1900-01-01T01:00:00Z\" AND (To:Null AND Cc:Null AND Bcc:Null)" + " AND Mailing-list:" + x

        res1 = solr.search(query,**param)#first get a list of mailing lists

        docs = res1.raw_response["response"]["numFound"]

        print("From + Date + Dest = " + str(docs))


        latex_table.append("From + Date + Dest & " + str(docs) + "\\\\")
        latex_table.append("\hline")





        query = "From:Null AND Date:\"1900-01-01T01:00:00Z\" AND NOT (To:Null AND Cc:Null AND Bcc:Null)"  + " AND Mailing-list:" + x

        res1 = solr.search(query,**param)#first get a list of mailing lists

        docs = res1.raw_response["response"]["numFound"]

        print("From + Date = " + str(docs))


        latex_table.append("From + Date & " + str(docs) + "\\\\")
        latex_table.append("\hline")





        query = "From:Null AND NOT Date:\"1900-01-01T01:00:00Z\" AND (To:Null AND Cc:Null AND Bcc:Null)"  + " AND Mailing-list:" + x

        res1 = solr.search(query,**param)#first get a list of mailing lists

        docs = res1.raw_response["response"]["numFound"]

        print("From + Dest = " + str(docs))


        latex_table.append("From + Dest & " + str(docs) + "\\\\")
        latex_table.append("\hline")






        query = "NOT From:Null AND Date:\"1900-01-01T01:00:00Z\" AND (To:Null AND Cc:Null AND Bcc:Null)"  + " AND Mailing-list:" + x

        res1 = solr.search(query,**param)#first get a list of mailing lists

        docs = res1.raw_response["response"]["numFound"]

        print("Date + Dest = " + str(docs))


        latex_table.append("Date + Dest & " + str(docs) + "\\\\")
        latex_table.append("\hline")





        query = "From:Null AND NOT Date:\"1900-01-01T01:00:00Z\" AND NOT (To:Null AND Cc:Null AND Bcc:Null)"  + " AND Mailing-list:" + x

        res1 = solr.search(query,**param)#first get a list of mailing lists

        docs = res1.raw_response["response"]["numFound"]

        print("From = " + str(docs))


        latex_table.append("From & " + str(docs) + "\\\\")
        latex_table.append("\hline")






        query = "NOT From:Null AND Date:\"1900-01-01T01:00:00Z\" AND NOT (To:Null AND Cc:Null AND Bcc:Null)" + " AND Mailing-list:" + x

        res1 = solr.search(query,**param)#first get a list of mailing lists

        docs = res1.raw_response["response"]["numFound"]

        print("Date = " + str(docs))


        latex_table.append("Date & " + str(docs) + "\\\\")
        latex_table.append("\hline")






        query = "NOT From:Null AND NOT Date:\"1900-01-01T01:00:00Z\" AND (To:Null AND Cc:Null AND Bcc:Null)" + " AND Mailing-list:" + x

        res1 = solr.search(query,**param)#first get a list of mailing lists

        docs = res1.raw_response["response"]["numFound"]

        print("Dest = " + str(docs))



        latex_table.append("Dest & " + str(docs) + "\\\\")
        latex_table.append("\hline")

        latex_table.append("\end{tabular}")
        latex_table.append("\end{center}")

        for x in latex_table:
            print(x)
