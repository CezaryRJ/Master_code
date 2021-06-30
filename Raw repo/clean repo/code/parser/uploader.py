import pysolr
from tqdm import tqdm

#handles uploading of parsed data to solr

def upload(host, data) :

	solr = pysolr.Solr(host)#connect

	print("Solr " + solr.ping()[215:227].replace("\""," ") + "\nIgnore previous error msg if there was one\n")

	acum = 0

	print("Files parsed = " + str(len(data)) + "\n\n\nUpload to Solr in progress")

	for file in tqdm(data):
		solr.add(file)#upload
		acum += len(file)


	print("\nAmmount of messages uploaded to Solr = " + str(acum))
