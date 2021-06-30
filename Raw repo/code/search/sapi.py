import numpy as np
import matplotlib.pyplot as plt



MAX_ROWS = 2147483647

def getQuery(response):
	return response.raw_response["responseHeader"]["params"]["q"]
	
def getParams(response):
	return response.raw_response["responseHeader"]["params"]

def getFacet(response):
	return response.facets["facet_fields"][next(iter(response.facets["facet_fields"]))]

	


def printResponse(inn):

	
	tmp = inn["responseHeader"]["params"]
	
	print("\n----------------------------------------------------------------------------------------++++\n\nPARAMETERS\n")
	
	for x in tmp:
		print(x + " = " , end = "")
		print(tmp[x])
	
	
	print("\n-----------------------------------------------------------------------------------------RESPONSE\n\n")
	
	tmp = inn["response"]["docs"]
	
	i=0
	
	cnt =""
	
	try :
		for x in tmp:
			print("\n>>> Headers >>>------------------------------------------------###################\n\n")
			cnt =  tmp[i]["Content"][0]
			del tmp[i]["Content"]
			for y in tmp[i]:
				
				print(y + " : ", end = "")
				print(tmp[i][y])
				
			print("\n>>> Content >>>---------------------------------------------------------------------------------->>>\n\n\n" + cnt)
			
			i = i + 1
			
			print("\n<<< END >>>----------------------------------------------------------------------------------<<<\n\n\nNEXT\n↓↓↓↓\n")
	except:
		pass
		
	try:
		i = 0
		tmp = inn["facet_counts"]["facet_fields"][inn["responseHeader"]["params"]["facet.field"]]
		
		print("\n-----------------------------------------------------------------------------------------FACET\n\n")
		
		for x in tmp:
			print(tmp[i] + " " + str(tmp[i + 1]))
			i = i + 2
			
	except:
		pass


def buildDatePoint(inn):
	
	if len(inn) < 5:
		#just year
		return "\"" + inn + "-01-01T00:00:00Z\""
	elif len(inn) < 8:
		#year and month
		return "\"" + inn + "-01T00:00:00Z\""
	if len(inn) < 11:
		#year month and date
		return "\"" + inn + "T00:00:00Z\""
	
def buildDateRange(start, end):
	
	a = ""
	b = ""
	if len(start) < 5:
		#just year
		a =  start + "-01-01T00:00:00Z"
	elif len(start) < 8:
		#year and month
		a =  start + "-01T00:00:00Z"
	elif len(start) < 11:
		#year month and date
		a =  start + "T00:00:00Z"
		
	if end.startswith("+"):
	 
		return "[" + a + " TO " + a + end + "]"
	
	else:
	
		if len(end) < 5:
			#just year
			b =  end + "-01-01T00:00:00Z"
		elif len(end) < 8:
			#year and month
			b =  end + "-01T00:00:00Z"
		elif len(end) < 11:
			#year month and date
			b =  end + "T00:00:00Z"
		
	
		return "[" + a + " TO " + b + "]"
		
	
	
	
def formatFacet(inn):
	tmp = getFacet(inn)
	i = 0
	x = []
	y = []
	while i < len(tmp):
		x.append(tmp[i])
		y.append(tmp[i+1])
		#print(tmp[i])
		#print(tmp[i+1])
		i=i+2
	
	return x,y
	
def makeBarGraph(x,y,name):

	y_pos = np.arange(len(x))
	plt.bar(y_pos, y)
	plt.xticks(y_pos, x)
	plt.savefig(name + ".png")
	plt.show()
	
def makeBarGraph(x,y):

	y_pos = np.arange(len(x))
	plt.bar(y_pos, y)
	plt.xticks(y_pos, x)
	plt.show()

	
	
	
	
	
	
	
	