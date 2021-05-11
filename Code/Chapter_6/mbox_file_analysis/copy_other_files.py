import os
import sys
from os import path

#file = open(sys.argv[1],"r")

slash = "/"

root = os.getcwd()

a = open("fa_result/maybe_mbox.txt","r")

a = a.readlines()

root = ""
try:
    root = "other_copy"
except:
    print("No argument given")
    exit()

try:
    print("Creating directory\n" + root)
    os.mkdir(root)
except:
    pass




out = open("out.txt","w")


for x in a:

    b = x.split(" ")[0].split("/")


    mlist = b[7]
    name = b[-1].strip()

    new_dir = []

    i = 7
    while i < len(b):
        new_dir.append(b[i])
        i = i + 1

    #printprint(new_dir)

    tmp = ""
    i = 0
    while i < len(new_dir)-1:
        tmp = tmp + slash + new_dir[i]

        print(os.getcwd() +  slash + root + tmp)


        try:

            #print("Creating directory\n" + root + tmp)
            os.mkdir(root + tmp)
            i = i + 1
        except:
            #print("hiuhfdhgiufyhgidufyhgudifyhgiu")

            i = i + 1





    os.system("cp " + x.strip() + " " + (root + tmp + slash + name))



out.close()
