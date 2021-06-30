import cleanarch
import os
import codecs
import sys
codecs.register_error("strict", codecs.replace_errors)

#import sys
#print(sys.getdefaultencoding())
#exit()

#every proceeding mail starts with "\n\n\nFrom"
#this means that we have to keep track of the last 4 lines seen
#to be able to determine if a mail has ended



	#=============================================================================

	#get all paths of files in all subdirectories
root_dir = "other_copy"#os.path.realpath(__file__))
file_set = []


print("\n\n\nScanning subdirectories\n\n\n")

for r, d, f in os.walk(root_dir):
	for file in f:
		file_set.append(os.path.join(r, file))



print("\n\n\n" + str(len(file_set)) + " files found\n\n\n")
	#=============================================================================

file_counter = 0


print("\n\n\nStarting parsing\n\n\n")

while file_counter < len(file_set):

	print(file_set[file_counter])
	cleanarch.clean(file_set[file_counter],file_set[file_counter] + "cl")
	sys.stdout = sys.__stdout__
	file_counter = file_counter + 1
