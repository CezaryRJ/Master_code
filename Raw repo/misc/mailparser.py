import os
import email
import _mailbox
import string
from dateutil.parser import *
#import datetime, pytz

#import re
		
		
def parseDate(a,filename):
	
	try :
		return parse(a).strftime("%Y-%m-%dT%H:%M:%S")
	except :
		return getDateFromFileName(filename)
	
def sanitizeDate(a,filename):
	
	a = a.split(" ")

	i = 0
	date = ""
	
	timezone = ""
	
	if len(a) > 4 : #if length is less than 4 something is not up to standard
		while i < 5 : 
		  date += a[i] + " " 
		  i += 1

	
		try : #timezone isnt mandatory, this might fail
			
			while i < len(a) :
			  timezone += " " + a[i]
			  i += 1
			  
		except :
			timezone = "-9999"
	
	else :
		timezone = "-9999"
			
	
	#print(date)
	#exit(0)

	return parseDate(date,filename), timezone.strip("()").strip("''")
	

def getDateFromFileName(filename):
	a = filename.split("/")
	a = a[len(a)-1].split(".")
	b = a[0].split("-")
	
	try:
		Integer(b[0]) #check if the name is actally a number
		return (a[0] + "-01T12:00:00")
	except:
		return "1900-01-01T12:00:00"
	
	
	
	


def parsefile(fileinn,mailing_list) :	

	print(fileinn)
	
	box = _mailbox.mbox(fileinn)

	iter = box.iterkeys()

	out = []
	
	header_missing = False
	
	stop = False
	
	for key in iter :

		msg = box.get_message(key)
		
		mail = {}
		#Aaccording to rfc4021 
		#https://tools.ietf.org/html/rfc4021#section-2.1
		
		
		#set these so they show up in solr 
		
		
		
		tmp = msg.get("Date")
		if not tmp is None:
			
			mail["Date"], mail["Timezone"] = sanitizeDate(tmp,fileinn)
			#mail["Timezone"] = getTimezone(tmp)
			
		else :
			mail["Date"] = "1900-01-01T12:00:00"
			mail["Timezone"] = -9999
		
		tmp = msg.get("From")
		if not tmp is None:
			mail["From"] = tmp
			print("From")
			exit(1)
		else :
			mail["From"] = "Null"
			header_missing = True
			stop = True
			
		tmp = msg.get("Sender")
		if not tmp is None:
			mail["Sender"] = tmp
		else :
			mail["Sender"] = "Null"
		
		tmp = msg.get("Reply-to")
		if not tmp is None:
			mail["Reply-to"] = tmp
		else :
			mail["Reply-to"] = "Null"
			
		tmp = msg.get("To")
		if not tmp is None:
			mail["To"] = tmp
		else :
			mail["To"] = "Null"
			
		tmp = msg.get("Cc")
		if not tmp is None:
			mail["Cc"] = tmp
		else :
			mail["Cc"] = "Null"

		tmp = msg.get("Message-ID")
		if not tmp is None:
			mail["Message-ID"] = tmp
		else :
			mail["Message-ID"] = "Null"
			
		tmp = msg.get("In-Reply-To")
		if not tmp is None:
			mail["In-Reply-To"] = tmp
		else :
			mail["In-Reply-To"] = "Null"	
		
			
		tmp = msg.get("Subject")
		if not tmp is None:
			mail["Subject"] = tmp
		else :
			mail["Subject"] = tmp
		
		mail["Mailing-list"] = mailing_list
		mail["File-location"] = fileinn
		
		mail["Had-missing-header"] = header_missing
		
			
		if not msg.is_multipart() : #This means that we are dealing with a regular text mail, no fancy parsing
			#print(box.get_message(key).get_payload())
			
			
			mail["Content"] = box.get_message(key).get_payload()
			
			#print(mail["Content"])
			
			if header_missing:
				if len(out) > 0: #there may be no content , this also means that if the first email in a file has an error it will be lost
					out[len(out)-1]["Content"] += "\n\n\n--------Past this is a email that had missing headers, it has therefore been appended to its predecessor--------\n\n\n" 
					out[len(out)-1]["Content"] += mail["Content"]
					out[len(out)-1]["Had-missing-header"] = header_missing
					header_missing = False
				else :
					mail["Content"] += "\n\n\n--------This is a email that had missing headers, it was the first in its file, and had nothing it could be appended on to\n\n\n" 
					mail["Content"] += mail["Content"]
					mail["Had-missing-header"] = header_missing
					header_missing = False
			else:
				out.append(mail)
			#print("---------------STR MSG---------------")
		
		else : #probably MIME mail parsing 
			
			mail["Content"] = ""
			for part in msg.walk():
				if part.get_content_type() == "text/plain":
					mail["Content"] += part.get_payload()
			#print(mime_mail["Content"])
			
			if header_missing:
				out[len(out)-1]["Content"] += mail["Content"]
				out[len(out)-1]["Had-missing-header"] = header_missing
				header_missing = False
			else:
				out.append(mail)
				
			#print("---------------MIME MSG---------------")
		#=============================================================================
	
		#print(msg)
		#print("\n\n\n\n\n\n")

	
		#if stop == True :
		#	mail = out[len(out)-1]
		#	print("FOUND ERROR")
		#	print(mail["Date"])
		#	print(mail["From"])
		#	print(mail["Sender"])
		#	print(mail["Reply-to"])
		#	print(mail["To"])
		#	print(mail["Cc"])
		#	print(mail["Message-ID"])
		#	print(mail["In-Reply-To"])
		#	print(mail["Subject"])
		#	print(mail["Content"])
			
		#	print("\n\n\n\nCHEACK THIS OUT")
			
		#	print(out[len(out)-1]["Content"])
			
		#	exit(1)
	
	#print("Date = " + out[0]["Date"])
	#print("From = " + out[0]["From"])
	#print("Sender = " + out[0]["Sender"])
	#print("Reply-to = " + out[0]["Reply-to"])
	#print("Subject = " + out[0]["Subject"])
	#print("Maling-list = " + out[0]["Mailing-list"])
	#print("File-location = " + out[0]["File-location"])
	return out;


	
	
	
	