import pysolr
import sys
from uploader import *

def get_month(inn):
    if inn =="jan":
        return "01"
    elif inn == "feb":
        return "02"
    elif inn == "mar":
        return "03"
    elif inn == "apr":
        return "04"
    elif inn == "may":
        return "05"
    elif inn == "jun":
        return "06"
    elif inn == "jul":
        return "07"
    elif inn == "aug":
        return "08"
    elif inn == "sep":
        return "09"
    elif inn == "oct":
        return "10"
    elif inn == "nov":
        return "11"
    elif inn == "dec":
        return "12"
    else:
        print(inn)
        exit()

a = open("rfc_bib.bib","r")

a = a.readlines()

i = 0

rfc_list = list()

out = open("editors.txt","w")

editors = set()

while i < len(a):

    rfc = dict()

    rfc["rfc"] = a[i][9:][:-2]

    i = i + 1

    while a[i] != "  }\n":

        tmp = a[i].strip().split("=")

        if tmp[0] != "publisher" and tmp[0] != "institution" and tmp[0] != "organization" and tmp[0] != "type" and tmp[0] != "number" and tmp[0] != "key": #these always contain the same data, so we skip them


            if tmp[0] == "year" or tmp[0] == "month":
                rfc[tmp[0]] = tmp[1][:-1]

            elif tmp[0] == "abstract":

                while a[i][-3:] != "},\n":
                    tmp[1] = tmp[1] + a[i]
                    i = i + 1

                rfc[tmp[0]] = tmp[1][1:][:-2]

            elif tmp[0] == "title":

                 rfc[tmp[0]] = tmp[1][2:][:-3]

            else:

                rfc[tmp[0]] = tmp[1][1:][:-2]




        i = i + 1


    rfc["date"] = rfc["year"] + "-" + get_month(rfc["month"]) + "-" + "01T00:00:00Z"

    rfc["author"] = rfc["author"].split(" and ")


    y = 0

    while y < len(rfc["author"]):
        if " (Ed.)" in rfc["author"][y]:

            if rfc["author"][y] not in editors:

                out.write(rfc["author"][y] + "\n")

                #print(rfc["author"][y])
                editors.add(rfc["author"][y])
                #rfc["author"].remove(rfc["author"][y])

            rfc["author"][y] = rfc["author"][y].replace("{","").replace("}","").replace(" (Ed.)","")



        elif rfc["author"][y][-1] == "}":
            rfc["author"][y] = rfc["author"][y].replace("{","").replace("}","")


            #rfc["author"][y] = rfc["author"][y].replace("}","").replace("{","").replace(" (Ed.)","")

            #print(rfc["author"][y])

        y = y + 1

    #print(rfc["author"])
    #exit()

    i = i + 2

    #for x in rfc:
    #    print(str(x) + " " + str(rfc[x]))
    #exit()


    rfc_list.append(rfc)

out.close()


upload("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + sys.argv[1],rfc_list)
