import pysolr

def upload(host, data) :

	solr = pysolr.Solr(host)
		
	x = 0
	
	acum = 0
	
	print("Files parsed = " + str(len(data)) + "\n\n\nUpload to Solr in progress")
	
	while x < len(data):
		solr.add(data[x])
		acum += len(data[x])
		x+=1
	
	print("\nAmmount of messages uploadet to Solr = " + str(acum))