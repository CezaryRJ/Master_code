import PySimpleGUI as sg


def test():
	print("this worked")


def res_box_out(x):
	tmp = []
	for y in x:
		if y != "Content":

			if isinstance(x[y], type([])):
				if x[y][0] != "Null":
					tmp.append(y + " : " + str(x[y][0]) + "\n")

			else:
				if x[y] != "Null":
					 tmp.append(y + " : " + str(x[y]) + "\n")

	return tmp

def update_headers(window,res1,values,index):
	tmp = ""

	x = res1.raw_response["response"]["docs"][index]
	tmp = ""
	for header in x:
		if header != "Content":

			if isinstance(x[header], type([])):
				if x[header][0] != "Null":
					tmp = tmp + header + "  :  " + str(x[header]) + "\n"

			else:
				if x[header] != "Null":
					 tmp = tmp + header + "	:  " + str(x[header]) + "\n"



	window.FindElement("output2").Update('')
	window.FindElement("output2").Update(tmp)


def get_edges_inn(msg,solr):

	param = {"debugQuery":"off",
				"rows" : 2147483647,
				"fl:To-address,Cc-address,Bcc-address,Reply-to-address,In-Reply-To-address,Subject"
			}

	edges = []
	res = solr.search(values["output1"],**param)#first get a list of mailing lists




def update_response(window,res1,param,values,index,update_res):
		tmp = ""
		for x in param:
			tmp = tmp + x + " : " + str(param[x]) + "\n"
		tmp1 =	""
		for x in param:
			tmp1 = tmp1 + x + " : " + str(param[x]) + "\n"

		if tmp != "":
			window.FindElement("output0").Update(tmp)
			window.FindElement("count0").Update(res1.raw_response["response"]["numFound"])



		window.FindElement("-ML-").Update('')

		list = []
		i = 0
		for x in res1.raw_response["response"]["docs"]:
			list.append(str(i) + ".  " + x["Subject"])
			i = i + 1


		print(res1.raw_response["response"]["docs"][index]["Content"])



		edges_out = []
		edges_inn = []

		for x in  res1.raw_response["response"]["docs"][index]["To-address"]:
			if x != "Null":
				edges_out.append(x)

		for x in  res1.raw_response["response"]["docs"][index]["Cc-address"]:
			if x != "Null":
				edges_out.append(x)

		for x in  res1.raw_response["response"]["docs"][index]["Bcc-address"]:
			if x != "Null":
				edges_out.append(x)

		for x in  res1.raw_response["response"]["docs"][index]["Reply-to-address"]:
			if x != "Null":
				edges_out.append(x)

		for x in  res1.raw_response["response"]["docs"][index]["In-Reply-To-address"]:
			if x != "Null":
				edges_out.append(x)

		if res1.raw_response["response"]["docs"][index]["References"] != "Null":
				edges_out.append(res1.raw_response["response"]["docs"][index]["References"])

		window.FindElement("edges_out").Update(edges_out)

		if update_res:
			window.FindElement("res_box").Update(list)

		update_headers(window,res1,values,index)
