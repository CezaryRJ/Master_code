import sys
import os



i = 0

while i < 8600:

    os.system("wget -F -nv -P /home/cezaryrj/wget/output/ https://datatracker.ietf.org/doc/rfc" + str(i))

    i = i + 1
