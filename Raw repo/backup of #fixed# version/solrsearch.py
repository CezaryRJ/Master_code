from urllib.request import urlopen
import sys


url = ('http://localhost:8983/solr/Master/select?q=' + str(sys.argv[1]) + ':' + str(sys.argv[2]) + '&wt=python')
connection = urlopen(url)
response = eval(connection.read())


#print(response['response']['docs'][0].keys())

print('\n\nDate: ' + str(response['response']['docs'][0]['Date'][0]))
print('From: ' + str(response['response']['docs'][0]['From'][0]))
print('Sender: ' + str(response['response']['docs'][0]['Sender'][0]))
print('Reply-to: ' + str(response['response']['docs'][0]['Reply-to'][0]))
print('To: ' + str(response['response']['docs'][0]['To'][0]))
print('Cc: ' + str(response['response']['docs'][0]['Cc'][0]))
print('Message-ID: ' + response['response']['docs'][0]['Message-ID'][0])
print('In-Reply-To: ' + response['response']['docs'][0]['In-Reply-To'][0])
print('Subject: ' + str(response['response']['docs'][0]['Subject'][0]))
print('Mailing-list: ' + str(response['response']['docs'][0]['Mailing-list'][0]))
print('File-location: ' + str(response['response']['docs'][0]['File-location'][0]))
print("\n\n" + response['response']['docs'][0]['Content'][0])


#in reply to
#message id 
#cc

#2. dec