import sys
import os


os.system("python fa.py /home/cezaryrj/new/ietf.org/")
os.system("python runcleaner_other.py /fa_result/maybe_mbox.txt"")
os.system("python create_file_list.py")
os.system("python comp_lists.py")

break

a = open("Missing_files.txt","r")

length = a.readline()

while length > 0:

    os.system("python runcleaner_other.py Missing_files.txt")

    os.system("python create_file_list.py")

    os.system("python comp_lists.py")

    a = open("Missing_files.txt","r")

    length = a.readline()
