import os
import email
import mailbox
import string
from dateutil.parser import *
		
def parseDate(a):
	return parse(a).strftime("%Y-%m-%dT%H:%M:%S")

def getTimezone(a):
	a = a.split(" ")
	return a[len(a)-1]

def parsefile(fileinn,mailing_list) :	

	print(fileinn)
	
	box = mailbox.mbox(fileinn)

	iter = box.iterkeys()

	out = []
	
	i = 0
	
	for key in iter :

		msg = box.get_message(key)
		
		#print(msg.as_string())
		
		
		
		#Aaccording to rfc4021 
		#https://tools.ietf.org/html/rfc4021#section-2.1
		
		header_error = False 
		
		tmp = msg.get("Date")
		if tmp is None :
			header_error = True
			
		tmp = msg.get("From")
		if tmp is None :
			header_error = True
			
		tmp = msg.get("To")
		if tmp is None :
			header_error = True
		
		if header_error is True : 
		
			file = open("error\\" + (mailing_list + str(i) + ".err"), "w",encoding="utf-8")
		
			#extract data for error report 
			
			tmp = msg.get("Date")
			if not tmp is None:
				file.write("Date: " + parseDate(tmp))
				file.write("Timezone: " + getTimezone(tmp))
				
			else :
		
				file.write("Date: 1900-00-00T0000:00")
				file.write("Timezone: -9999")
			
			tmp = msg.get("From")
			if not tmp is None:
				file.write("From: " + tmp)
			else :
				file.write("From: Null")
				#print(msg.as_string())
				#exit(1)
				
			tmp = msg.get("Sender")
			if not tmp is None:
				file.write("Sender: " + tmp)
			else :
				file.write("Sender: Null")
			
			tmp = msg.get("Reply-to")
			if not tmp is None:
				file.write("Reply-to: " + tmp)
			else :
				file.write("Reply-to: Null")
				
			tmp = msg.get("To")
			if not tmp is None:
				file.write("To: " + tmp)
			else :
				file.write("To: Null")
				
			tmp = msg.get("Cc")
			if not tmp is None:
				file.write("Cc: " + tmp)
			else :
				file.write("Cc: Null")

			tmp = msg.get("Message-ID")
			if not tmp is None:
				file.write("Message-ID: " + tmp)
			else :
				file.write("Message-ID: Null")
				
			tmp = msg.get("In-Reply-To")
			if not tmp is None:
				file.write("In-Reply-To: " + tmp)
			else :
				file.write("In-Reply-To: Null")	
			
				
			tmp = msg.get("Subject")
			if not tmp is None:
				file.write("Subject: " + tmp)
			else :
				file.write("Subject: Null")
			
			file.write("Mailing-list: " +  mailing_list)
			file.write("File-location: " + fileinn)
			
				
			if not msg.is_multipart() : #This means that we are dealing with a regular text mail, no fancy parsing
				#print(box.get_message(key).get_payload())
				
				
				file.write(box.get_message(key).get_payload())
				
				#print(mail["Content"])
				
				#print("---------------STR MSG---------------")
			
			else : #probably MIME mail parsing 
				
				content = ""
				for part in msg.walk():
					if part.get_content_type() == "text/plain":
						content += part.get_payload()
				#print(mime_mail["Content"])
				file.write(content)
				#print("---------------MIME MSG---------------")
			#=============================================================================
			
			print("\n\n\n\n\n" + msg.as_string())
			file.write("\n\n\n\n\n" + msg.as_string())
			header_error = False
			file.close()
			print("File has been closed")
			#exit(1)
		
		i = i + 1
	
	#print("Date = " + out[0]["Date"])
	#print("From = " + out[0]["From"])
	#print("Sender = " + out[0]["Sender"])
	#print("Reply-to = " + out[0]["Reply-to"])
	#print("Subject = " + out[0]["Subject"])
	#print("Maling-list = " + out[0]["Mailing-list"])
	#print("File-location = " + out[0]["File-location"])
	return out;


	
	
	
	