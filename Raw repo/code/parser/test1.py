import pysolr

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/test/")

a = print("Solr " + solr.ping()[215:227].replace("\""," ") + "\nIgnore previous error msg\n")

