#This a modified version of the clearch script found in the mailman program
#modified by Cezary RJ



#! @PYTHON@

# Copyright (C) 2001-2018 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

"""Clean up an .mbox archive file.

The archiver looks for Unix-From lines separating messages in an mbox archive
file.  For compatibility, it specifically looks for lines that start with
"From " -- i.e. the letters capital-F, lowercase-r, o, m, space, ignoring
everything else on the line.

Normally, any lines that start "From " in the body of a message should be
escaped such that a > character is actually the first on a line.  It is
possible though that body lines are not actually escaped.  This script
attempts to fix these by doing a stricter test of the Unix-From lines.  Any
lines that start "From " but do not pass this stricter test are escaped with a
> character.

Usage: cleanarch [options] < inputfile > outputfile
Options:
    -s n
    --status=n
        Print a # character every n lines processed

    -q / --quiet
        Don't print changed line information to standard error.

    -n / --dry-run
        Don't actually output anything.

    -h / --help
        Print this message and exit
"""

import re
import sys
import getopt
import mailbox

#import paths
#from Mailman.i18n import C_

cre = re.compile(mailbox.UnixMailbox._fromlinepattern)

# From RFC 2822, a header field name must contain only characters from 33-126
# inclusive, excluding colon.  I.e. from oct 41 to oct 176 less oct 072.  Must
# use re.match() so that it's anchored at the beginning of the line.
fre = re.compile(r'[\041-\071\073-\176]+')




def escape_line(line, lineno, quiet, output):
    if output:
        sys.stdout.write('|' + line)



def clean(inn,out):

    quiet = False
    output = True
    status = -1


    file = open(inn,"rb")

    lineno = 0
    statuscnt = 0
    messages = 0
    prevline = None
	
    sys.stdout = open(out, 'wb') #redirect stdout to file
	
	
    while True:
       
        lineno += 1
        line = file.readline()
        
        if not line:
            break
        if line.startswith('From '):

            if cre.match(line):
                # This is a real Unix-From line.  But it could be a message
                # /about/ Unix-From lines, so as a second order test, make
                # sure there's at least one RFC 2822 header following
                nextline = file.readline()
				
                lineno += 1
	if not nextline:
		# It was the last line of the mbox, so it couldn't have
		# been a Unix-From
		escape_line(line, lineno, quiet, output)
		break
	fieldname = nextline.split(':', 1)
	if len(fieldname) < 2 or not fre.match(nextline):
		# The following line was not a header, so this wasn't a
		# valid Unix-From
		escape_line(line, lineno, quiet, output)
		if output:
			sys.stdout.write(nextline)
	else:
                    # It's a valid Unix-From line
                    messages += 1
                    if output:
                        # Before we spit out the From_ line, make sure the
                        # previous line was blank.
	if prevline is not None and prevline != '\n':
		sys.stdout.write('\n')
	sys.stdout.write(line)
	sys.stdout.write(nextline)
            else:
                # This is a bogus Unix-From line
                escape_line(line, lineno, quiet, output)
        elif output:
            # Any old line
            sys.stdout.write(line)
        if status > 0 and (lineno % status) == 0:
            sys.stderr.write('#')
            statuscnt += 1
            if statuscnt > 50:
                print >> sys.stderr
                statuscnt = 0
        prevline = line
   # print >> sys.stderr, str(messages) +  " messages found"


