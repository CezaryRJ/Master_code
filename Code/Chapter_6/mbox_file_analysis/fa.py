from __future__ import division
import os
import sys
import codecs

codecs.register_error("strict", codecs.replace_errors)



slash = "\\"

if sys.platform == "win32":
	print("\n\nRunning on Windows\n")
else:
	slash = "/"
	print("\n\nRunning on Unix\n")

root_dir = ""

try :
	root_dir = sys.argv[1]
	print("Reading directory " + root_dir + "\n")
except:
	print("No argument given")
	exit()

#counters
file_count = 0

definetly_mailbox = 0
def_mbox = []
size_def_mbox = 0

maybe_mailbox = 0
maybe_mbox = []
size_maybe_mbox = 0

definetly_not_mailbox = 0
not_mbox = []
size_not_mbox = 0

total_size = 0

pos_mbox_dir = []

for r,d,f in os.walk(root_dir):

	for file in f:

		absolute_path = os.path.join(r, file)

		#print(absolute_path)

		tmp = absolute_path.split(".")[-1] #file extention
		size = os.path.getsize(absolute_path)
		if(tmp == "mail"):#if file has "mail" extention, then it is an mbox file
			definetly_mailbox = definetly_mailbox + 1
			def_mbox.append(absolute_path + " " + str(size))
			size_def_mbox = size_def_mbox + size

		if(tmp != "mail" and tmp != "mailcl"):

			a = open(os.path.join(r,file)).readline()[:4]

			if(a == "From"): #if first 4 characters are "From" then it may be an mbox

				maybe_mailbox = maybe_mailbox + 1
				maybe_mbox.append(absolute_path) #+ " " + str(size))
				size_maybe_mbox = size_maybe_mbox + size
				pos_mbox_dir.append(absolute_path)

			else:
				definetly_not_mailbox = definetly_not_mailbox + 1
				not_mbox.append(absolute_path + " " + str(size))
				size_not_mbox = size_not_mbox + size



		file_count = file_count + 1
		total_size = total_size + size


print("File count = " + str(file_count))
print("Definetly mbox = " + str(definetly_mailbox))
print("Maybe mbox = " + str(maybe_mailbox))
print("Definetly not mbox = " + str(definetly_not_mailbox))


print("\nSize in bytes")
print("Total size = " + str(total_size))
print("Def mbox = " + str(size_def_mbox) + " " + str((size_def_mbox/total_size)*100) + "%")
print("Maybe mbox = " + str(size_maybe_mbox) + " " + str((size_maybe_mbox/total_size)*100) + "%")
print("Not mbox = " + str(size_not_mbox) + " " + str((size_not_mbox/total_size)*100) + "%")

print("\n")

out = open("fa_result" + slash + "fa_result.txt","w")

out.write("File count = " + str(file_count) + "\n")
out.write("Definetly mbox = " + str(definetly_mailbox) + "\n")
out.write("Maybe mbox = " + str(maybe_mailbox) + "\n")
out.write("Definetly not mbox = " + str(definetly_not_mailbox) + "\n")


out.write("\nSize in bytes" + "\n")
out.write("Total size = " + str(total_size) + "\n")
out.write("Def mbox = " + str(size_def_mbox) + " " + str((size_def_mbox/total_size)*100) + "%" + "\n")
out.write("Maybe mbox = " + str(size_maybe_mbox) + " " + str((size_maybe_mbox/total_size)*100) + "%" + "\n")
out.write("Not mbox = " + str(size_not_mbox) + " " + str((size_not_mbox/total_size)*100) + "%" + "\n")

out.close()

out = open("fa_result" + slash + "def_mbox.txt","w")
for x in def_mbox:
	out.write(x+"\n")
out.close()


out = open("fa_result" + slash + "maybe_mbox.txt","w")
for x in maybe_mbox:
	out.write(x+"\n")
out.close()

out = open("fa_result" + slash + "not_mbox.txt","w")
for x in not_mbox:
	out.write(x+"\n")
out.close()

out = open("fa_result" + slash + "pos_mbox_dir.txt","w")
for x in pos_mbox_dir:
	out.write(x+"\n")
out.close()


if (len(def_mbox) + len(maybe_mbox) + len(not_mbox) != file_count):
	print("\n-----Something went wrong-----\n")

if(size_def_mbox + size_maybe_mbox + size_not_mbox != total_size):
	print("\n\n" + str(size_def_mbox + size_maybe_mbox + size_not_mbox) + " != " + str(total_size))
	print("\n-----Something went wrong with size-----\n")
