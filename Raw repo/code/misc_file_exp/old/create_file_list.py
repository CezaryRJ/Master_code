import os 
import sys

slash = "\\"

if sys.platform == "win32":
	print("\n\nRunning on Windows\n")
else:
	slash = "/"
	print("\n\nRunning on Unix\n")
    

root_dir = "/home/cezaryrj/ietf/cezaryrj/misc_file_exp/other_clean/"


out = open("clean_list.txt","w")

print(root_dir)

for r, d, f in os.walk(root_dir):
	
	for file in f:
		out.write(os.path.join(r, file) + "\n")
        

out.close()
		
