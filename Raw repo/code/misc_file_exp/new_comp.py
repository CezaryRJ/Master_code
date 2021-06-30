import sys
import os


slash = "\\"

if sys.platform == "win32":
	print("\n\nRunning on Windows\n")
else:
	slash = "/"
	print("\n\nRunning on Unix\n")


a = open("fa_result" + slash + "maybe_mbox.txt","r")

b = open("scan_res.txt","r")


a_list = a.readlines()

b_list = b.readlines()


print("List 1 length = " + str(len(a_list)))

print("List 2 length = " + str(len(b_list)))

i = 0
for x in a_list:
	if  x.strip().split(slash)[-1] != b_list[i].strip().split(slash)[-1]:
		print(x)
		print(b_list[i])
		exit()
	i = i + 1
