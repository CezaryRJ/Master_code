import os
import email
from email.utils import *
import mailbox
import string
import time
import re
from dateutil.parser import *


#this is the part that parses the actuall mbox  files

def addField(name,mail,msg):#adds a field
	tmp = msg.get(name)
	if not tmp is None:
		mail[name] = tmp.strip()#strip whitespace
	else :
		mail[name] = "Null"




def addMultiIdField(name,mail,msg):#adds a multivalued field

	tmp = msg.get(name)#pull data


	if not tmp is None and tmp != "": #see if anyting was pulled

		mail[name] = tmp

		tmp = msg.get_all(name)

		for value in tmp:#split, as described in thesis

			ids = re.split(' |,|\t|\n|\r',value)

			out = list()

			for x in ids:

				a = x.split("><")

				if len(a) > 1:
					out.append(a[0] + ">")
					out.append("<" + a[-1])

					for y in a[1:][:-1]:
						out.append("<" + y + ">")

				else:
					out.append(x)



			final = list()

			for x in out:#check if string has @ in it, if yes, include it
				if "@" in x:
					final.append(x)
				elif len(x) > 1 and x[0] == "<" and x[-1] == ">":
					final.append(x)

					#print("\n")
					#print(mail[name])
					#print(x)


			if len(final) > 0:
				mail[name + "-ID"] = final
			else:
				mail[name + "-ID"] = ["Null"]

				#print("\n")
				#print(mail[name])
				#print(out)
				#print(final)

	else:	#if nothing was pulled, set to null

		mail[name] = "Null"
		mail[name + "-ID"] = ["Null"]







def addAddressField(name,mail,msg):#adds solr field assosiated with a email address field
	tmp = msg.get(name)

	if not tmp is None and tmp != "":#if anything was extracted

		mail[name] = tmp

		tmp = msg.get_all(name, [])
		tmp = getaddresses(tmp)

		i = 0

		tmp_name = []
		tmp_address = []


		while i < len(tmp) :

			if tmp[i][0] != '' : #check if name was extracted
				tmp_name.append(tmp[i][0])


			if tmp[i][1] != '' : #check if address was extracted
				tmp_address.append(tmp[i][1])


			i = i + 1

		if not tmp_name: #if empty then add null
			tmp_name.append("Null")

		if not tmp_address : #if empty then add null
			tmp_address.append("Null")


		mail[name + "-name"] = tmp_name
		mail[name + "-address"] = tmp_address

	else :
		mail[name] = "Null"
		mail[name + "-name"] = ["Null"]
		mail[name + "-address"] = ["Null"]

def printmail(inn):
	print("\n")
	for key, value in inn.items():
		print(key, ':', value)

	print("\n\n\n")

def parseDate(a):#converts date to solr format

	try :
		return time.strftime("%Y-%m-%dT%H:%M:%S",parsedate(a))
	except :
		return "1900-01-01T0001:00"


def getTimezone(a):#not used
	a = a.split(" ")
	return a[len(a)-1]

def parsefile(fileinn,mailing_list) : #main method that parses the mbox file

	#print(fileinn)


	box = mailbox.mbox(fileinn)

	iter = box.iterkeys()

	out = []

	for key in iter :

		msg = box.get_message(key)

		mail = {}
		#Aaccording to rfc4021
		#https://tools.ietf.org/html/rfc4021#section-2.1


		#set these so they show up in solr

		tmp = msg.get("Date")
		if not tmp is None:


			mail["Date"] = parseDate(tmp)
			mail["Date-raw"] = tmp
			mail["Timezone"] = getTimezone(tmp)



		else :

			mail["Date"] = "1900-01-01T0001:00"
			mail["Date-raw"] = "Null"
			mail["Timezone"] = -9999



		addAddressField("From",mail,msg)

		addAddressField("Sender",mail,msg)

		addAddressField("Reply-to",mail,msg)

		addAddressField("To",mail,msg)

		addAddressField("Cc",mail,msg)

		addAddressField("Bcc",mail,msg)

		addField("Message-ID",mail,msg)

		addMultiIdField("In-Reply-To",mail,msg)

		addMultiIdField("References",mail,msg)

		addField("Comments",mail,msg)

		addField("Subject",mail,msg)

		#print(mail["Message-ID"])
		#print(mail["In-Reply-To"])

		mail["Mailing-list"] = mailing_list
		mail["File-location"] = fileinn


		if not msg.is_multipart() : #This means that we are dealing with a regular text mail, no fancy parsing
			#print(box.get_message(key).get_payload())


			mail["Content"] = box.get_message(key).get_payload()

			#print(mail["Content"])
			out.append(mail)
			#print("---------------STR MSG---------------")

		else : #probably MIME mail parsing

			mail["Content"] = ""
			for part in msg.walk():
				if part.get_content_type() == "text/plain":
					mail["Content"] += part.get_payload()
			#print(mime_mail["Content"])
			out.append(mail)
			#print("---------------MIME MSG---------------")
		#=============================================================================

		#printmail(mail)

		#exit(0) #------------------------


	#print("Date = " + out[0]["Date"])
	#print("From = " + out[0]["From"])
	#print("Sender = " + out[0]["Sender"])
	#print("Reply-to = " + out[0]["Reply-to"])
	#print("Subject = " + out[0]["Subject"])
	#print("Maling-list = " + out[0]["Mailing-list"])
	#print("File-location = " + out[0]["File-location"])

	return out;
