from html.parser import HTMLParser
import requests
from bs4 import BeautifulSoup


rfc_id = 2822#start, there is nothing before around 850 however
limit = 3000


ppl = dict()

errors = list()

while rfc_id < limit:

    try: #the connection may fail
        print("RFC" + str(rfc_id))
        print('https://datatracker.ietf.org/doc/rfc' + str(rfc_id) + '/')
        vgm_url = 'https://datatracker.ietf.org/doc/rfc' + str(rfc_id) + '/'
        html_text = requests.get(vgm_url,timeout=5).text
        soup = BeautifulSoup(html_text, 'html.parser')


        names = list()

        adr = list()

        for a in soup.find_all('a', href=True):
                if a.get('href')[:8] == "/person/":
                    adr.append(a.get('href')[8:])
                    print("person = " + a.get('href'))

        for a in soup.find_all('a'):

            if str(a)[:12] == "<a href=\"/wg":
                if str(a)[-6:] == "WG</a>":
                    print("Working group = " + str(a).split(">")[1].split(" ")[0])
            #print("-----------------------------------------------------------------------------------------")



        for a in soup.find_all('span', {'class' : ''}):
            names.append(a.text)
            a.get(a.text)


        i = 0

        while i < len(adr):

            try:
                ppl[names[i]].add(adr[i])
            except:
                ppl[names[i]] = set()
                ppl[names[i]].add(adr[i])

            print("\n" + names[i])
            print(adr[i] + "\n")

            i = i + 1



    except:

        print("Error getting RFC" + str(rfc_id)) #print the rfc that failed
        errors.append(rfc_id)


    exit()
    rfc_id = rfc_id + 1


out = open("ppl.txt","w",encoding="utf-8")

for x in ppl:
    out.write(str(x) + "\n")

    for y in ppl[x]:
        if "%" not in y:
            out.write(y + "\n")

    out.write("\n\n")

out.close()


out = open("errors.txt","w",encoding="utf-8")
for x in errors:
    out.write(str(x) + "\n")

out.close()
