import pysolr
import os
import sys
import codecs
codecs.register_error("strict", codecs.replace_errors)



MAX_ROWS = 2147483647

core1 = sys.argv[1]

core2 = sys.argv[2]

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/" + core1 + "/")


param = {
"rows" : MAX_ROWS
}

res1 = solr.search("*:*",**param)


sum1 = 0
for x in res1.docs :
    
    sum1 = sum1 + len(x["Content"])
    
avg = sum1/res1.raw_response