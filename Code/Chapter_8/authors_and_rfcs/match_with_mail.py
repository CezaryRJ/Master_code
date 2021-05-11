from frame import *
import sys

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]


def get_orig(name,list):
    out = ""
    for x in list:
        out = out + x + " "

    out = out + name

    return out


def parse_mail_name(name,list):
    out = ""
    for x in list:

        try:
            out = out + x[0].upper() + "." + " "
        except:
            pass

    out = out + name

    return out


solr_bib = connect_to_solr(sys.argv[1])

solr_mail = connect_to_solr(sys.argv[2])

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-name",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

slash = get_slash()

res = solr_mail.search("*:*",**param)

i = 0

names = dict()

#prepare names from the email archives
while i < len(res.raw_response["facet_counts"]["facet_fields"]["From-name"]):

    a = res.raw_response["facet_counts"]["facet_fields"]["From-name"][i]
    b = a.split(" ")

    out = ""

    if len(b) > 1:

        for x in b:
            try:
                if x[0] == "(": #remove anything that starts with a paranthesis
                    b.remove(x)
            except:
                pass

    try:
        names[b[-1]].append(b[:-1])
    except:
        names[b[-1]] = list()
        names[b[-1]].append(b[:-1])


    i = i + 2


#print(names["Carpenter"])



param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"author",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

res = solr_bib.search("*:*",**param)

author_names = dict()

i = 0
while i < len(res.raw_response["facet_counts"]["facet_fields"]["author"]):
    a = res.raw_response["facet_counts"]["facet_fields"]["author"][i]
    b = a.split(" ")
#    print(b)
    try:
    #    print(b)
        author_names[b[-1]].append(b[:-1])
    except:
        author_names[b[-1]] = list()
        author_names[b[-1]].append(b[:-1])


    i = i + 2


#print(author_names["Welzl"])

ppl = dict()

for x in names.keys(): #exact match on last name

    if x in author_names:
        for y in author_names[x]:

            rfc_name = get_orig(x,y)
            #print(rfc_name)
            for z in names[x]:
                mail_name = parse_mail_name(x,z)

                if mail_name == rfc_name:
                    try:
                        ppl[mail_name] = ppl[mail_name] + 1
                    except:
                        ppl[mail_name] = 1



s = dict(sorted(ppl.items(), key=lambda item: item[1]))

print(s)



#count
count = dict()
print(len(ppl))
for x in s:

    try:
        count[s[x]] = count[s[x]] + 1
    except:
        count[s[x]] = 1

sum = 0
for x in count:
    print(x)
    print((count[x]/len(ppl))*100)
    sum = sum + (count[x]/len(ppl))*100


print(sum)
