a = open("found_mbox.txt","r")

slash = "\\"

b = open("clean_list.txt","r")

dict_a = {}


tmp = 0

i1 = 0
i2 = 0

for line in a:

	tmp = line.split(slash)[-1:][0][:-1]
	dict_a[line.split(slash)[-1:][0][:-1]] = True
	i1 = i1+1
	
for line in b:
	dict_a.pop(line.split(slash)[-1:][0][:-3])
	i2 = i2+1
	
	
for key in dict_a:
	print(key)

print(len(dict_a))

print("Insert = " + str(i1))

print("Removes = " + str(i2))