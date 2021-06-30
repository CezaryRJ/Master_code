import pysolr
import uploader



host = "localhost"
port = "8983"
core = "test"
user = "cezaryrj"
password = "SolrisNice1995"

database = []
doc = {}
doc["Content"] = ["N","dfg","n","n","n"]
database.append(doc)


#uploader.upload("http://" +user + ":" + password + "@"+host+ ":" + str(port) + "/solr/" + core,database)


solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/test/")


param = {"debugQuery":"off",
"rows" : 10,
"facet":"off", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1,
"stats":"off",
"stats.field":"Mailing-list"

}

res1 = solr.search("*:*",**param)#first get a list of mailing lists
print(res1.docs[0]["Content"][0])
print(res1.docs[0]["Content"][1])