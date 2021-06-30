import os
import sys

import codecs
codecs.register_error("strict", codecs.replace_errors)

SETTING_DIR = "C:\\Users\\Cezary\\Documents\\GitHub\\Master\\code\\settings.txt"zzzz

def read_settings():
	try:
		f = open(SETTING_DIR, "r")
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


archive_location = settings["archive_location"]#"D:\\ietf-archive"#"C:\\Users\\Cezary\\Documents\\GitHub\\Master\\code\\testdata"


database = []


	#=============================================================================
	
	#get all paths of files in all subdirectories
root_dir = archive_location

print(root_dir)

file_set ={}
file_set["Other"] = 0


file_size = {}
file_size["Other"] = 0

print("\n\nScanning subdirectories\n\n")

tmp = "a"

empty_file = 0
unmarked_mbox = 0
empty_file_not_mbox = 0
mail = 0
empty_mail = 0
non_empty_other = 0
other_file = 0


found_mbox = []

for r, d, f in os.walk(root_dir):
	
	for file in f:
		
		tmp = os.path.join(r, file).split(".")[-1]
		
		if(tmp == "mail"):
			mail = mail + 1
			if(os.path.getsize(os.path.join(r,file)) == 0):
				empty_mail = empty_mail + 1
		

		
		if(tmp != "mail" and tmp != "mailcl"):
			other_file = other_file + 1
			if(os.path.getsize(os.path.join(r,file)) == 0):
				empty_file_not_mbox = empty_file_not_mbox + 1
			else:	
				a = open(os.path.join(r,file)).readline()[:4]
				if(a == "From"):
					unmarked_mbox = unmarked_mbox + 1
					found_mbox.append(os.path.join(r, file))
	

empty_file = empty_file_not_mbox + empty_mail
			
sum = 0
sum_size = 0
for a in file_set:
	if(a == "mail" or a == "mailcl"):
		print(a + " " + str(file_set[a]) + "|	  Bytes = " + str(file_size[a]))
	sum = sum + file_set[a]
	sum_size = sum_size + file_size[a]
	

print("\nSum .mail files = " + str(mail) + "\nSum empty .mail = " + str(empty_mail))

print("\nSum other files = " + str(other_file) + "\nSum unmarked_mbox = " + str(unmarked_mbox) + "\nSum empty other = " + str(empty_file_not_mbox))
print("\nUnclassified = " + str(other_file-unmarked_mbox-empty_file_not_mbox))

out = open("found_mbox.txt","w")

for x in found_mbox:
	out.write(x + "\n")

out.close()


#inn = open("found_mbox.txt","r")


#inn1 = open(b.strip(),"r")
#inn1 = inn1.read()
#print(inn1)
