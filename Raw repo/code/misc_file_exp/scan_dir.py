import sys
import os

slash = "\\"

if sys.platform == "win32":
	print("\n\nRunning on Windows\n")
else:
	slash = "/"
	print("\n\nRunning on Unix\n")

root_dir = "other_copy"



file_set = []

for r, d, f in os.walk(root_dir):
	for file in f:
		file_set.append(os.path.join(r, file))
		#print(os.path.join(r, file))

print(len(file_set))


i = 0
for x in file_set:
	file_set[i] = (x.split(slash)[-1])
	#print(file_set[i])
	i = i + 1


a = open("fa_result" + slash + "maybe_mbox.txt","r")
a_list = a.readlines()

i = 0
for x in a_list:
	a_list[i] = x.split(slash)[-1].strip()
	#print(a_list[i])
	i = i + 1

print("Before")
print("List 1 length = " + str(len(a_list)))

print("List 2 length = " + str(len(file_set)))

for x in file_set:
	for y in a_list:
		if x.strip() == y.strip():
			a_list.remove(y)
			break





print("\n\nAfter")

print(a_list)


print("List 1 length = " + str(len(a_list)))

print("List 2 length = " + str(len(file_set)))
