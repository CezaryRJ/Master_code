import pysolr

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
