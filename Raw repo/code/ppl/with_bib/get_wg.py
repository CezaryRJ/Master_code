import pysolr
import sys
from uploader import *
from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup
from frame import *


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

rfc_list = dict()

while i < len(a): #parse the bib

    doc = dict()

    tmp = a[i].split("=")

    while tmp[0].strip() != "author":

        i = i + 1

        tmp = a[i].split("=")

    tmp_author = tmp[1].split(" and ")
    authors_out = list()

    if len(tmp_author) == 1:
        authors_out.append(tmp_author[0][1:][:-3])
    else:

        authors_out.append(tmp_author[0][1:])

        for x in tmp_author[1:][:-1]:
            authors_out.append(x)

        authors_out.append(tmp_author[-1][:-3])

    doc["author"] = authors_out




    while tmp[0].strip() != "title":

        i = i + 1

        tmp = a[i].split("=")
    doc["title"] = tmp[1][2:][:-4]


    while tmp[0].strip() != "number":

        i = i + 1
        tmp = a[i].split("=")
    doc["number"] = tmp[1][1:][:-3]


    while tmp[0].strip() != "year":

        i = i + 1
        tmp = a[i].split("=")

    year = tmp[1][:-2]

    i = i + 1
    tmp = a[i].split("=")
    month = get_month(tmp[1][:-2])

    doc["date"] = year + "-" + month + "-01T00:00:00Z"


#    if int(doc["number"]) > 8000:
    rfc_list[doc["number"]] = doc

    #print(doc["number"])
    #print(doc["author"])

    #if "1835" == doc["number"]:
    #    exit()

    i = i + 13

#    print(rfc_list[doc["number"]])
ppl = dict()
errors = list()
retry = True

wg = set()

for x in tqdm(rfc_list):
    #print(x)
    retry = True
    while retry:
        try:
            #print("RFC" + str(x))
            #print('https://datatracker.ietf.org/doc/rfc' + str(x) + '/')
            vgm_url = 'https://datatracker.ietf.org/doc/rfc' + str(x) + '/'
            html_text = requests.get(vgm_url,timeout=5).text
            soup = BeautifulSoup(html_text, 'html.parser')



            for a in soup.find_all('a'):
                tmp = str(a).split("/")
                if tmp[1] == "wg" and tmp[-3] == "about":

                    wg.add(tmp[2])

                    #print(x)
                    #print(tmp[2])
                    #print("Working group = " + str(a).split(">")[1].split(" ")[0])



                i = i + 1

            retry = False

        except :
            print("Error getting RFC" + str(x) + "\nRetrying") #print the rfc that failed

#now we have the names
out = open("wg.txt","w")
for x in wg:
    out.write(str(x) + "\n")
