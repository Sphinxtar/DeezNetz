#!/usr/bin/python3
# Deez Netz Server Client Sweeper
# reads deezhosts file of one hostname per line
# checks http://hostname:8142/OK and gets system status from client
# builds XML tree of statuses in memory 
# applies deezNetz.xsl and writes /var/www/html/deezNetz.js
import requests
from lxml import etree as ET
protocol = "http://"
port = 8142
path = "/OK"


def sweepDeez():
	xmldoc = ["<?xml version=\"1.0\"?><hosts>"]
	hoststyle = open('hostdoc.xsl')
	hostroot = hoststyle.read()
	hoststyle.close()
	hostxslt = ET.XML(hostroot)
	hosttransform = ET.XSLT(hostxslt)

	doc = open('/usr/share/deez/deezhosts', 'r')
	for line in doc:    
		host = line.strip('\n')
		url = protocol+host+":"+str(port)+path
		try:
			response = requests.get(url,timeout=4)
			if (response.status_code != 200):
				status = "<?xml version=\"1.0\"?><host name=\"" +host+"\"><status>RED</status></host>"
			else:
				status = response.text.strip()
		except Exception as ex:
			status = "<?xml version=\"1.0\"?><host name=\"" +host+"\"><status>RED</status></host>"
#		print("STATUS: "+status)
		statxml = ET.XML(status)
		xmldoc.append(str(hosttransform(statxml)))
	doc.close()
	xmldoc.append("</hosts>")
	return("".join(xmldoc))

print(sweepDeez())
