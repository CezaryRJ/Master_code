from frame import *
import sys
import os
import codecs
from tqdm import tqdm
codecs.register_error("strict", codecs.replace_errors)


solr = connect_to_solr(sys.argv[1])

iteration_limit = int(sys.argv[2])

param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":2 #can only have more than one name if more than 1 msg sendt

}


error_list = list()

try:
    os.mkdir("errors")
    os.mkdir("people")
except:
    pass

remove_list = {
"Internet-Drafts@ietf.org",
"internet-drafts@ietf.org",
"notifications@github.com",
"iesg-secretary@ietf.org",
"rfc-editor@rfc-editor.org",
"noreply@github.com",
"feedback@oneoffice.jp",
"noreply@ietf.org",
"ietf-secretariat-reply@ietf.org",
"Internet-Drafts@ns.ietf.org",
"Null"
}






slash = get_slash()

res1 = solr.search("*:*",**param)

tmp = res1.raw_response["facet_counts"]["facet_fields"]["From-address"]

address_list = list()

i = 0

while i < len(tmp):
    address_list.append(tmp[i])
    i = i + 2

for x in remove_list:
    address_list.remove(x)


param_name = {"debugQuery":"off",
"rows" : 2147483647,
"fl" : "From-name" ,
"facet":"off"
}

param_adr = {"debugQuery":"off",
"rows" : 2147483647,
"fl" : "From-address" ,
"facet":"off"
}

agents = list()


print(str(len(address_list)) + " addresses found")


pbar = tqdm(total=(len(address_list)))

i = 0

iter_count = 0

while i < len(address_list):

    #print(address_list[i])

    #print(len(address_list))
    try:
        name_set = set()
        adr_set = set()

        new_adr = set()
        new_adr.add(address_list[i])

        new_name = set()

        while True:

            if iter_count < iteration_limit:

                #print(iter_count)

                new_adr = new_adr.difference(adr_set)
                new_name = new_name.difference(name_set)

                #print(new_adr)
                #print(new_name)

                adr_set |= new_adr
                name_set |= new_name

                if len(new_adr) == 0 and len(new_name) == 0:
                    break


                for x in new_adr:

                    names = solr.search("From-address:" + "\"" + x + "\"",**param_name)

                    #print("NAMES = " + str(names.raw_response["response"]["numFound"]))

                    for y in names.raw_response["response"]["docs"]:
                        if len(y["From-name"]) == 1:
                            new_name.add(y["From-name"][0])


                try:
                    new_name.remove("Null")
                except:
                    pass


                for x in new_name:

                    adr = solr.search("From-name:" + "\"" + x + "\"",**param_adr)

                    #print("ADR = " + str(names.raw_response["response"]["numFound"]))

                    for y in adr.raw_response["response"]["docs"]:
                        if len(y["From-address"]) == 1:
                            #print(y)
                            new_adr.add(y["From-address"][0])

                try:
                    new_adr.remove("Null")
                except:
                    pass

                iter_count = iter_count + 1
            else:
                break



            for x in remove_list:
                try:
                    new_adr.remove(x)
                except:
                    pass


            #print(new_adr)
            #print(new_name)

        agents.append((name_set,adr_set))
        iter_count = 0

        print("\n\n\n")
        print(name_set)
        print(adr_set)


    except:

        error_list.append(address_list[i])

    i = i + 1
    pbar.update(1)

    for x in adr_set:
        try:
            address_list.remove(x)
        except:
            pass


    i = 0



i = 0

for x in agents:

    out = open("people/" + str(i) + ".txt","w")

    for y in x[0]:
        out.write(str(y) + "\n")

    out.write("\n")

    for y in x[1]:
        out.write(str(y) + "\n")

    i = i + 1

out = open("errors/error.txt","w")
for x in error_list:
    out.write(str(x) + "\n")

out.close()
