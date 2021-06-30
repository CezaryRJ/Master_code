from frame import *
import sys



param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":100,
"facet.sort":"count",
"facet.mincount":1

}


param_authors = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"wg",
"facet.limit":100,
"facet.sort":"count",
"facet.mincount":1

}


top_20 = 20

slash = get_slash()

matching_lists = open("match.txt","r").readlines()

blacklist = open("blacklist.txt","r").readlines()

solr = connect_to_solr("ietf-archive-final-v2")

solr_authors = connect_to_solr("author")

for x in matching_lists:

    tmp = list()

    print("\n\n" + str(x))

    out = open("res/" + x[:-1] +".txt","w")

    out.write(x + "\n\n")

    res1 = solr.search("Mailing-list:" + x[:-1],**param)

    #print(res1.raw_response["facet_counts"]["facet_fields"]["From-address"])

    i = 0
    while i < len(res1.raw_response["facet_counts"]["facet_fields"]["From-address"]):

        if res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i].lower() not in tmp:
            tmp.append(res1.raw_response["facet_counts"]["facet_fields"]["From-address"][i].lower())

        i = i + 2

    for y in blacklist:
        try:
            tmp.remove(y[:-1].lower())
        except:
            pass



    top_20_poster = tmp[:20]

#    print(top_20_poster)

    results = list()

    for y in top_20_poster:

        res = solr_authors.search("address:" + "\"" + y + "\"",**param_authors)

        if res.raw_response["response"]["numFound"] > 0:

            #print(y)

            i = 0

        #    print(res.raw_response["facet_counts"]["facet_fields"]["wg"])

            while i < len(res.raw_response["facet_counts"]["facet_fields"]["wg"]):

                if res.raw_response["facet_counts"]["facet_fields"]["wg"][i] == x[:-1]:
                #    print(res.raw_response["facet_counts"]["facet_fields"]["wg"][i])
                    results.append(y)
                    break

                i = i + 2

    print(results)

    for y in results:
        out.write(str(y) + "\n")

    out.close()
