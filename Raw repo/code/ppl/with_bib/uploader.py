import pysolr
from tqdm import tqdm

def upload(solr, data) :


	print("Solr " + solr.ping()[215:227].replace("\""," ") + "\nIgnore previous error msg if there was one\n")


	for file in tqdm(data):
		solr.add(file)
