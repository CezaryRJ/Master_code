from urllib.request import urlopen

connection = urlopen('http://ls.hpc.uio.no:8983/solr/Master/select?facet=on&facet.field=Content&q=*%3A*&rows=0&start=0&wt=python&facet.limit=1000000000')
response = eval(connection.read())


i = 0
acum = 0

#print("LENGTH = " + str(len(response['facet_counts']['facet_fields']['Content'])))
print("COUNTING")
while i < len(response['facet_counts']['facet_fields']['Content']):
	acum = acum + int(response['facet_counts']['facet_fields']['Content'][(i+1)])
	i = i+2

print("TOKENS = " + str(acum))
print("TERMS = " + str(i))

#print(response['facet_counts']['facet_fields']['Content'][0])
#print(response['facet_counts']['facet_fields']['Content'][1])

