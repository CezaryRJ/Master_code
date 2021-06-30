import sys

slash = "\\"

if sys.platform == "win32":
	print("\n\nRunning on Windows\n")
else:
	slash = "/"
	print("\n\nRunning on Unix\n")


a = open("fa_result" + slash + "pos_mbox_dir.txt","r")

b = open("clean_list.txt","r")


a_list = {}


b_list = {}

a = open("fa_result" + slash + "pos_mbox_dir.txt","r")

a_list = a.readlines()

b_list = b.readlines()


print("List 1 length = " + str(len(a_list)))

print("List 2 length = " + str(len(b_list)))


for x in b_list:
	for y in a_list:
		if x.strip().split(slash)[-1][:-2] == y.strip().split(slash)[-1]:
			a_list.remove(y)
			break
			
			

print("Missing files = " + str(len(a_list)))

out = open("missing_files.txt","w")

for x in a_list:
	out.write(x)

out.close()


