import pysolr
import sys
#“,+,-,/,!,[,],{,},^,~
#+,-,~,!


def fix_adr(inn):
    #print(inn)
    out = ""
    for x in inn:

        if x == "\"":
            out = out + "\\"

        out = out + x

    out = out.strip()
    #print( "\"" + out + "\"")
    return  "\"" + out + "\""

def get_slash():
    slash = "\\"

    if sys.platform == "win32":
    	print("\n\nRunning on Windows\n")
    else:
    	slash = "/"
    	print("\n\nRunning on Unix\n")

    return slash

def connect_to_solr(core):
    try:
        return pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + core)
    except:
        print("Could not connect to core " + core)
        exit()

def max(solr,query,facet_field):

    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":facet_field,
    "facet.limit":1,
    "facet.sort":"count",
    "facet.mincount":1
    }

    res = solr.search(query,**param)

    return res.raw_response["facet_counts"]["facet_fields"][facet_field][0]



def min(solr,query,facet_field):

    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":facet_field,
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":1
    }

    res = solr.search(query,**param)

    return res.raw_response["facet_counts"]["facet_fields"][facet_field][-2]





def avg(solr,query,facet_field):

    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":facet_field,
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":1
    }

    res = solr.search(query,**param)

    i = 1

    acum = 0

    while i < len(res.raw_response["facet_counts"]["facet_fields"][facet_field]):
        acum = acum + res.raw_response["facet_counts"]["facet_fields"][facet_field][i]
        i = i + 2

    return acum/(len(res.raw_response["facet_counts"]["facet_fields"][facet_field])/2)



def unique(solr,query,facet_field):

    param = {"debugQuery":"off",
    "rows" : 0,
    "facet":"on", #if this is set to "off" then no facet will be returned
    "facet.field":facet_field,
    "facet.limit":-1,
    "facet.sort":"count",
    "facet.mincount":1
    }

    res = solr.search(query,**param)

    i = 0

    out = list()

    while i < len(res.raw_response["facet_counts"]["facet_fields"][facet_field]):
        out.append(res.raw_response["facet_counts"]["facet_fields"][facet_field][i])
        i = i + 2

    return out
