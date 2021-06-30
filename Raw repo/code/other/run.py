import email
import uploader
import os
import mailparser
import time
import sys
from datetime import datetime
from tqdm import tqdm

import codecs
codecs.register_error("strict", codecs.replace_errors)

def read_settings():
	try:
		f = open("settings.txt", "r")
	except:
		print("No settings file found, aborting")
		exit(0)
		
	settings = {}

	line = f.readline().strip("\n").split(" ")
	while line != ['']:
		
		#print(line)
		settings[line[0]] = line[2]
		line = f.readline().strip("\n").split(" ")

	return settings
	
settings = read_settings()

host = settings["host"]
port = settings["port"]
core = settings["core"]

user = ""
password = ""

filetype = settings["filetype"]

archive_location = settings["archive_location"]#"D:\\ietf-archive"#"C:\\Users\\Cezary\\Documents\\GitHub\\Master\\code\\testdata"



print("\n\nHost = " + host + "\nPort = " + str(port) +"\nCore = " + core + "\nFiletype = " + filetype + "\nArchive location = " + archive_location + "\n\nSolr location = " + settings["solr_location"])


try :
	user = settings["user"]
	password = settings["password"] #this is a horrible thing to do but it will have to suffice  
except :
	print("\nNo username and password provided")

	
if user != "" :
	print("\nUser = " + user )
	
	if password != "": 
		print("Password has been provided")
	else : 
		print("No password, aborting")
		exit(2)








database = []


start_time = time.time()



	#=============================================================================
	
	#get all paths of files in all subdirectories
root_dir = archive_location
file_set = []


now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("\n\n--------Start time =", current_time)


print("\n\nScanning subdirectories\n\n")

for r, d, f in os.walk(root_dir):
	for file in f:
		
		file_set.append(os.path.join(r, file))
		#print(os.path.join(r, file))
		

print(str(len(file_set)) + " files found\n\n")
	#=============================================================================	

error_list = []


print("\n\nParsing in progress\n\n")

for file in tqdm(file_set):
    #print(file)
		
    mail_list = file.split(settings["slash"])
    
    #print(mail_list[len(mail_list)-2])

    database.append(mailparser.parsefile(file,mail_list[len(mail_list)-2]))
    
	#print(database)
    
    #exit()

		
		


		
print("\n\n\nProcessing done, starting Solr\n\n\n")

os.system(settings["solr_location"].replace("\\","/")+"/bin/solr start")



if user == "" :

	uploader.upload("http://"+host+ ":" + str(port) + "/solr/" + core,database)
	
else :
	uploader.upload("http://" +user + ":" + password + "@"+host+ ":" + str(port) + "/solr/" + core,database)
	


print("\n\n\nUpload done, happy searching !\n\n\n")


elapsed_time = time.time() - start_time




print("\n\n\nShutting down Solr")
os.system(settings["solr_location"].replace("\\","/")+"/bin/solr stop -all")


print("Minutes elapsed since beginning of parsing = " + str(elapsed_time/60))
