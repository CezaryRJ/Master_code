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

def facet_to_list(facet):

    out = list()

    if len(facet) < 3:
        out.append(facet[1])
        out.append(0)
        return out


    i = 1

    while i < len(facet):
        out.append(facet[i])
        i = i + 2

    return out
