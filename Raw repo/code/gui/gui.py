import PySimpleGUI as sg
from tools import *
import pysolr

param = {"debugQuery":"off",
			"rows" : 20,
			"facet":"on", #if this is set to "off" then no facet will be returned
			"facet.field":"Mailing-list",
			"facet.limit":-1,
			"facet.sort":"count",
			"facet.mincount":1

			}





sg.theme('Dark')	# Add a touch of color
# All the stuff inside your window.


sort_options = []


items = ["*",
		 "Date",
		 "Timezone",
		 "From",
		 "From-name",
		 "From-address",
		 "Sender",
		 "Sender-name",
		 "Sender-address",
		 "Reply-to",
		 "Reply-to-name",
		 "Reply-to-address",
		 "To",
		 "To-name",
		 "To-address",
		 "Cc",
		 "Cc-name",
		 "Cc-address",
		 "In-Reply-To",
		 "In-Reply-To-name",
		 "In-Reply-To-address",
		 "Message-ID",
		 "References",
		 "Comments",
		 "Subject",
		 "Miling-list",
		 "File-location",
		 "id"
		]

layout1 = [
		[sg.Text("Date point")],
		[sg.Text("Date"),sg.InputText()],
		[sg.Text("\nDate range")],
		[sg.Text("Start"),sg.InputText()],
		[sg.Text("End "),sg.InputText()],

		[sg.Text("\nSearch fields")],
		[sg.Text("Results start "),sg.InputText(0)],
		[sg.Text("Results end  "),sg.InputText(),sg.Checkbox("MAX")],

		[sg.Text("Sort by"),sg.InputCombo(sort_options, size=(20, 1), key="sort")],

		[sg.InputCombo(items, size=(20, 1), key="items_combobox0"),sg.InputText(key="test0")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox1"),sg.InputText(key="test1")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox2"),sg.InputText(key="test2")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox3"),sg.InputText(key="test3")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox4"),sg.InputText(key="test4")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox5"),sg.InputText(key="test5")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox6"),sg.InputText(key="test6")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox7"),sg.InputText(key="test7")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox8"),sg.InputText(key="test8")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox9"),sg.InputText(key="test9")],
		[sg.InputCombo(items, size=(20, 1), key="items_combobox10"),sg.InputText(key="test10")],
		[sg.Text()],
		[sg.Text("Facet options"),sg.Checkbox("ON"),sg.Text("Sort by"),sg.InputCombo(sort_options, size=(20, 1), key="sort_facet")],
		[sg.Text("Field "),sg.InputText()],
		[sg.Text("Rows"),sg.InputText(),sg.Checkbox("MAX")],
		[sg.Text("Min count "),sg.InputText()],
		[sg.Text("Max count"),sg.InputText()],
		[sg.Button("Search",key="s1")],
		[sg.Text("\nAdvaced search")],
		[sg.Multiline("*:*",size=(60,10), key='output1', autoscroll=False)],

		[sg.Button('Search',key="s2"),sg.Button('Connect'),	sg.Button('Refresh')]





		]  # identify the multiline via key option



layout2 = [[sg.Text('Content output', font='Any 15')],
				[sg.Multiline(size=(105,40), key='-ML-', autoscroll=False, reroute_stdout=True, write_only=True, reroute_cprint=True)],

				[sg.Listbox(values=[], size=(105, 10),enable_events=True,key="res_box")],
				[
				sg.Frame('Search options',[

				[sg.Button("<- Next"),sg.Button("Previous ->")],
				[sg.Text("Quick access")],
				[sg.Button("Reply-to"),sg.Button("In-Reply-to")]

				]),

				sg.Frame('Message options',
				[
				[sg.Button("Write to file")]
				]),

				sg.Frame('Program output',
				[
				[sg.Multiline(size=(50,5),autoscroll=True,write_only=True)]
				]),

			]]


layout3 = [

		[sg.Text('Solr response                                   ', font='Any 15'),sg.Button("Refresh")],
			[sg.Text("Results found")],
			[sg.InputText(size=(20,1),key="count0")],
			[sg.Text("Message headers                                                                   ")],
			[sg.Multiline(size=(60,20), key='output2', autoscroll=False,write_only=True)],
			[sg.Text("Outgoing edges                                                                                   ")],
			[sg.Listbox(values=[], size=(60, 5),enable_events=True,key="edges_out")],
			[sg.Text("Incoming edges                                                                                  ")],
			[sg.Listbox(values=[],size=(60,5), key='edges_inn')],
			[sg.Text("Parameters                                                                            ")],
			[sg.Multiline(size=(60,10), key='output0', autoscroll=False,  write_only=True)],

			[
		sg.Frame('Program options',[

		[sg.Button('Connection'),sg.Button("Read settings from file")],
		[sg.Button('Exit')]



		  ])]
			]  # identify the multiline via key option




layout = [
	[
		sg.Column(layout1),
		sg.VSeperator(),
		sg.Column(layout2),
		sg.VSeperator(),
		sg.Column(layout3)
	]
]

# Create the Window
window = sg.Window('Test', layout).Finalize()
#window.Maximize()

window.move(50,0)

res1 = {}

solr = pysolr.Solr("http://cezaryrj:SolrisNice1995@localhost:8983/solr/ietf-archive-unclean/")

current_index = 0

while True:

	event, values = window.read()

	if event in (None, 'Exit'): # if user closes window or clicks cancel
		break
	elif event == "s1":
		update_response(window,res1,param,0)
		print(values)

	elif event == "s2":

		res1 = solr.search(values["output1"],**param)#first get a list of mailing lists
		update_response(window,res1,param,values,0,True)

	elif event == "Connect":
		print("tmp")

	elif event == "res_box":
		current_index = int(values["res_box"][0].split(".")[0])
		update_response(window,res1,param,values,current_index,False)


window.close()
