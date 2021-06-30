from report_errors import *
from top_contributors import *

core = "ietf"

host = "ls.hpc.uio.no:8983"

addr = "http://cezaryrj:SolrisNice1995@" + host + "/solr/" + core + "/"

solr = pysolr.Solr(addr)


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

res1 = solr.search("*:*",**param)#first get a list of mailing lists

calc_contr(solr,res1)

#report_errors(addr)
