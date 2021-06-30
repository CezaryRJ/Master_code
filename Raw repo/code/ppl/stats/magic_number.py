from frame import *
import sys
from tqdm import tqdm


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"number",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

slash = get_slash()
solr = connect_to_solr("rfc")

res1 = solr.search("*:*",**param)

rfc_id = list()

i = 0

while i < len(res1.raw_response["facet_counts"]["facet_fields"]["number"]):
    rfc_id.append(res1.raw_response["facet_counts"]["facet_fields"]["number"][i])
    i = i + 2





solr_author = connect_to_solr("author")


solr_email = connect_to_solr("ietf-archive-final-v2")

for x in tqdm(rfc_id):

    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"author",
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":1

    }

    res1 = solr.search("number:" + str(x),**param)

    i = 0


    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":"author",
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":1

    }

    authors = list()

    while i < len(res1.raw_response["facet_counts"]["facet_fields"]["author"]):

        check = solr_author.search("name:" + "\"" + res1.raw_response["facet_counts"]["facet_fields"]["author"][i] + "\"")

        if check.raw_response["response"]["numFound"] > 0:
            authors.append(res1.raw_response["facet_counts"]["facet_fields"]["author"][i])
            #print(x)
            #print(res1.raw_response["facet_counts"]["facet_fields"]["author"][i])

        i = i + 2


    if len(authors) > 0:


        param = {"debugQuery":"off",
        "rows" : 1
        }

        date = solr.search("number:" + x)

        date = date.raw_response["response"]["docs"][0]["date"][0]

        #print(date)

        sum = 0

        param = {"debugQuery":"off",
        "rows" : 1
        }

        authors_full = dict()

        for y in authors:#get theit email addresses
            adr = solr_author.search("name:" + "\"" + y + "\"",**param)
            authors_full[y] = adr.raw_response["response"]["docs"][0]["address"]



        for y in authors_full:
            for z in authors_full[y]:

            
                tmp = solr_email.search("From-address:" + "\"" + z + "\" AND Date:[" + date +"-6MONTHS" + " TO " + date + "]",**param)

                sum = sum + tmp.raw_response["response"]["numFound"]


        if sum > 0:
            print(x)
            print(authors)
            print("MSG SENDT BEFORE PUBLICATION = " + str(sum))
