import email
import uploader
import os
import mailparser
import time

import codecs
codecs.register_error("strict", codecs.replace_errors)

#import sys
#print(sys.getdefaultencoding())
#exit()

#every proceeding mail starts with "\n\n\nFrom"
#this means that we have to keep track of the last 4 lines seen 
#to be able to determine if a mail has ended


database = []


start_time = time.time()

	#=============================================================================
	
	#get all paths of files in all subdirectories
root_dir = os.path.dirname(os.path.realpath(__file__))
file_set = []



print("\n\n\nScanning subdirectories\n\n\n")

for r, d, f in os.walk(root_dir):
	for file in f:
		if file.endswith(".mail"):
			file_set.append(os.path.join(r, file))
			#print(os.path.join(r, file))
		

print("\n\n\n" + str(len(file_set)) + " files found\n\n\n")
	#=============================================================================	

file_counter = 0

error_list = []


print("\n\n\nStarting parsing\n\n\n")

while file_counter < len(file_set):
	try:
		
		mail_list = file_set[file_counter].split("/")
		
		#print("Mail List" + mail_list[len(mail_list)-2])

		database.append(mailparser.parsefile(file_set[file_counter],mail_list[len(mail_list)-2]))
		file_counter += 1

	except Exception as e:
		
		error_log = open("errors/" + str(type(e).__name__) + str(file_counter) + ".err","w") # x to create new file
		print("\n\n" + file_set[file_counter] + "\nError type = " + str(type(e).__name__) + "\n" + str(e) + "\n\n" + str(e.args) + "\n\n")
		error_log.write("\n\n" + file_set[file_counter] + "\nError type = " + str(type(e).__name__) + "\n" + str(e) + "\n\n" + str(e.args) + "\n\n")
		error_log.close()
		file_counter += 1


		
print("\n\n\nProcessing done, uploading to Solr\n\n\n")


uploader.upload("http://localhost:8983/solr/Master",database)


print("\n\n\nUpload done, happy searching !\n\n\n")


elapsed_time = time.time() - start_time

print("Minutes elapsed since beginning of parsing = " + str(elapsed_time/60))



