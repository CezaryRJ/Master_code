import os
import email
import _mailbox
import string
		
def parsefile(fileinn,mailing_list) :	

	print(fileinn)
	
	box = _mailbox.mbox(fileinn)

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
			mail["Date"] = tmp
		else :
			mail["Date"] = "Null"
		
		tmp = msg.get("From")
		if not tmp is None:
			mail["From"] = tmp
		else :
			mail["From"] = "Null"
			
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
	


	
	#print("Date = " + out[0]["Date"])
	#print("From = " + out[0]["From"])
	#print("Sender = " + out[0]["Sender"])
	#print("Reply-to = " + out[0]["Reply-to"])
	#print("Subject = " + out[0]["Subject"])
	#print("Maling-list = " + out[0]["Mailing-list"])
	#print("File-location = " + out[0]["File-location"])
	return out;


	
	
	
	