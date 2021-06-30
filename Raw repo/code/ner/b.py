import pysolr
import os
import spacy

def printres(out, val):
	space = 10
	left_over = space-len(str(val))
	
	out.write(val)
	
	while left_over > 0:
		out.write(" ")
		left_over = left_over - 1
	

def addspace(out,name):
	space = 25
	left_over = space-len(name)
	while left_over > 0:
		out.write(" ")
		left_over = left_over -1
		
def fill_dict(inn,dict,field):

	for x in inn:

		tmp = x[field][0]
			
		try:
			dict[tmp] = dict[tmp] + 1
		except:	
			doc = nlp(tmp)
			
			for entity in doc.ents:
				if entity.label_ == "PERSON": #if classified as a person, include
					#print(entity.text, entity.label_)
					dict[entity.text] = 1
					
					
		
MAX_ROWS = 2147483647
solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/ietf-archive/")


dict_from = {}
dict_To_name = {}
dict_Sender_name = {}
dict_Reply_to_name = {}
dict_Cc_name = {}
dict_Bcc_name = {}
dict_In_Reply_To_name = {}

nlp = spacy.load("en_core_web_sm")

rows = 500

param = {"debugQuery":"off",
"rows" : rows,
"fl":"From-name,Sender-name,Reply-to-name,To-name,Cc-name,Bcc-name,In-Reply-To-name",
"facet":"off", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

print("Querying solr")

res1 = solr.search("*:*",**param)#first get a list of mailing lists

print("Calculating stats")


fill_dict(res1,dict_from,"From-name")

fill_dict(res1,dict_To_name,"To-name")

fill_dict(res1,dict_Sender_name,"Sender-name")

fill_dict(res1,dict_Reply_to_name,"Reply-to-name")

fill_dict(res1,dict_Cc_name,"Cc-name")

fill_dict(res1,dict_Bcc_name,"Bcc-name")

fill_dict(res1,dict_In_Reply_To_name,"In-Reply-To-name")


		
longest = dict_from

if len(dict_To_name) > len(longest):
	longest = dict_To_name

if len(dict_Sender_name) > len(longest):
	longest = dict_Sender_name	

if len(dict_Reply_to_name) > len(longest):
	longest = dict_Reply_to_name
	
if len(dict_Cc_name) > len(longest):
	longest = dict_Cc_name
	
if len(dict_Bcc_name) > len(longest):
	longest = dict_Bcc_name

if len(dict_In_Reply_To_name) > len(longest):
	longest = dict_In_Reply_To_name
	
print("Printing")
	
out = open("ppl.txt","w")

out.write("                         F         T         S         RT        CC        BCC       IRT       SUM\n")

for x in longest:
	
	sum = 0
	
	out.write(x)
	addspace(out,x)
	
	try:
		printres(out, str(dict_from[x]))
		sum = sum + dict_from[x]
	except:
		printres(out, str(0))
		
	
	try:
		printres(out, str(dict_To_name[x]))
		sum = sum + dict_To_name[x]
	except:
		printres(out, str(0))
	
	
	try:
		printres(out, str(dict_Sender_name[x]))
		sum = sum + dict_Sender_name[x]
	except:
		printres(out, str(0))
		

	try:
		printres(out, str(dict_Reply_to_name[x]))
		sum = sum + dict_Reply_to_name[x]
	except:
		printres(out, str(0))
		
	
	try:
		printres(out, str(dict_Cc_name[x]))
		sum = sum + dict_Cc_name[x]
	except:
		printres(out, str(0))
		
	
	try:
		printres(out, str(dict_Bcc_name[x]))
		sum = sum + dict_Bcc_name[x]
	except:
		printres(out, str(0))
		
		
	try:
		printres(out, str(dict_In_Reply_To_name[x]))
		sum = sum + dict_In_Reply_To_name[x]
	except:
		printres(out, str(0))
		
	printres(out, str(sum))
	
	
	out.write("\n")
	
out.close()



