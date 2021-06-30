import sys
from tqdm import tqdm
from frame import *

solr = connect_to_solr(sys.argv[1])

from_adr = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"From-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

sender_adr = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Sender-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

reply_to_adr = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Reply-to-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

to_adr = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"To-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

cc_adr = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Cc-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

bcc_adr = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Bcc-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

in_reply_to_adr = {"debugQuery":"off",
"rows" :0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"In-Reply-To-address",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

params = []
params.append(from_adr)
params.append(sender_adr)
params.append(reply_to_adr)
params.append(to_adr)
params.append(cc_adr)
params.append(bcc_adr)
params.append(in_reply_to_adr)

responses = []

email = dict()

slash = get_slash()

i = 0
for x in params:

    responses.append(solr.search("*:*",**x).raw_response["facet_counts"]["facet_fields"][x["facet.field"]])
    print(x["facet.field"] + " " + str(len(responses[i])))
    i = i + 1


for x in tqdm(responses):
        i = 0
        while i < len(x):
            try:
                email[x[i]] = email[x[i]] + x[i+1]
            except:
                email[x[i]] = x[i+1]

            i = i + 2


out = open("most_active.txt","w")

for x in email.keys():
    out.write(str(x) + " " + str(email[x]) + "\n")

out.close()
