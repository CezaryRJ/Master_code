Code used to anlisyzxxe the varion categorise of files as described in the thesis
There are several executable files in this directory.
In order for everything to work as expected they need to be executed in a specific order.

fa.py
This program is responsible for counting and creating lists to specify which files belong to which category.

copy_other_files.py
This file uses one of the lists created by the previous program to copy all files that may be mbox files, aka category 2.

runcleaner_other.py
This is just a pre configured run of cleanarch.

Run.py
This and other files are just pre configured runs of the mailparser
