from frame import *
import sys
import numpy
from tqdm import tqdm

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":150,
"facet.sort":"count",
"facet.mincount":1

}


param_authors = {"debugQuery":"off",
"rows" : 0
}



start = 1990
year = start




top_20 = 20

slash = get_slash()

matching_lists = open("match.txt","r").readlines()

blacklist = open("blacklist.txt","r").readlines()

solr = connect_to_solr("ietf-archive-final-v2")

solr_authors = connect_to_solr("author")

mean = dict()
div = dict()

while year != 2021:

    print(year)

    author_count = list()


    for x in tqdm(matching_lists):

        tmp = list()

        #print("\n\n" + str(x))


        res1 = solr.search("Date:[" + str(year) + "-01-01T00:00:00Z TO "+str(year) + "-01-01T00:00:00Z+1YEAR] AND Mailing-list:" + x[:-1],**param)

    #    print(res1.raw_response["response"]["numFound"])

        if res1.raw_response["response"]["numFound"] > 0:
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



            top_20_poster = tmp[:100]

        #    print(top_20_poster)

            results = list()

            count = 0

            for y in top_20_poster:


                res = solr_authors.search("address:" + "\"" + y.replace(":","\:") + "\" AND wg:" + x[:-1],**param_authors)


                if res.raw_response["response"]["numFound"] > 0:#id an uthor found see if working group matches

                    results.append(y)
                    count = count + 1

            #print(results)
                                    #non-authors/authors
            if count > 0 :
                author_count.append((len(top_20_poster)-count)/count)


            if len(results) > 0:#if no results, do not track stats

                out = open("res/" + x[:-1] + "-" + str(year) +".txt","w")

                out.write(x + "\n\n")

                for y in results:
                    out.write(str(y) + "\n")

                out.close()

    #print(author_count)
    if len(author_count) > 0:
        mean[year] = numpy.mean(author_count)
        div[year] = numpy.std(author_count)

        print("\n")
        print(mean[year])
        print(div[year])

    year = year + 1

print("\n\nMEAN\n")
print("\\addplot[color=red] coordinates {")
for x in mean:
    print("(" + str(x) + "," + str(mean[x]) + ")")

print("};\n\n")

print("\\addplot[name path=us_top,color=blue!70] coordinates {")
for x in mean:
    print("(" + str(x) + "," + str(mean[x]+((div[x])/2)) + ")")

print("};\n\n")

print("\\addplot[name path=us_down,color=blue!70] coordinates {")
for x in mean:
    print("(" + str(x) + "," + str(mean[x]-((div[x])/2)) + ")")

print("};\n\n")
