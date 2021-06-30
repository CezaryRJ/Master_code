import pysolr
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from sapi import *

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@ls.hpc.uio.no:8983/solr/test/")


param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Mailing-list",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":1

}

res1 = solr.search("*:*",**param)#first get a list of mailing lists



param = {"debugQuery":"off",
"rows" : 0,
"facet":"on", #if this is set to "off" then no facet will be returned
"facet.field":"Date",
"facet.limit":-1,
"facet.sort":"count",
"facet.mincount":0

}

if not os.path.exists('Timelines'):
    os.makedirs('Timelines')

figure(num=None, figsize=(200, 15), dpi=100, facecolor='w', edgecolor='k')

x = 0
f = ""
while x < len(getFacet(res1)):
	if not os.path.exists("Timelines/" + getFacet(res1)[x]):
		os.makedirs('Timelines/' + getFacet(res1)[x])
		
	print(getFacet(res1)[x])
	
	f = open("Timelines/" +getFacet(res1)[x] +"/" + getFacet(res1)[x] +"-timeline.txt","w")
	f.write("-------#####------->    " + getFacet(res1)[x] + "\n")
	res = solr.search("Mailing-list:" + getFacet(res1)[x],**param)


	tmp = {}
	a = getFacet(res)
	i = 0
	while i < len(a):
		try: 
			tmp[a[i][:7]] = tmp[a[i][:7]] + 1
		except:
			tmp[a[i][:7]] =  1
		
		i = i + 2

	i = 0
	key = []
	value = []
	for i in sorted (tmp.keys()) :  
		f.write(i + " " + str(tmp[i]) + "\n") 
		key.append(i)
		value.append(tmp[i])
		#print(i + " " + str(tmp[i]) + "\n") 
		
	
	f.close()
	plt.plot(key, value) 
		 
	plt.title('Timeline', fontsize=14)
	plt.xlabel('Year-Month', fontsize=14)
	plt.ylabel('Emails received', fontsize=14)
	plt.grid(True)
	
	#plt.show()
	plt.savefig("Timelines/" +getFacet(res1)[x] +"/" + getFacet(res1)[x] +"-timeline.png")
	x = x + 2
	
	
	 
#for x in res.debug:#
#	print(x)
#	print(res.debug[x])
