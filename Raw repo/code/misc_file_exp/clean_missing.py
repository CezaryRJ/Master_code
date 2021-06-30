import sys
import os


os.system("python fa.py /home/cezaryrj/new/ietf.org/")
os.system("python runcleaner_other.py fa_result/maybe_mbox.txt")
os.system("python create_file_list.py")
os.system("python comp_list.py")


a = open("missing_files.txt","r")

length = a.readlines()

prev = length

while length > 0:

    os.system("python runcleaner_other.py missing_files.txt")

    os.system("python create_file_list.py")

    os.system("python comp_list.py")

    a = open("missing_files.txt","r")

    length = a.readlines()
    
    if length >= prev:
        break
