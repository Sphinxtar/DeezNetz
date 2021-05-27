#!/usr/bin/python3
# Deez Netz Server Client Sweeper
# reads deezhosts file of one hostname per line
# checks http://hostname:8142/OK and gets system status from client
# builds XML tree of statuses in memory 
# applies deezNetz.xsl and writes /var/www/html/deezNetz.js
import certifi
import urllib3
from lxml import etree as ET

protocol = "http://"
port = 8142
path = "/OK"
http = urllib3.PoolManager(timeout=3.0)


def sweepDeez():
	red = 0
	yellow = 0
	green = 0
	reddoc = ["<?xml version=\"1.0\"?><hosts><bg>red</bg><msg>OK</msg>"]
	yellowdoc = ["<?xml version=\"1.0\"?><hosts><bg>yellow</bg><msg>ERR</msg>"]
	greendoc = ["<?xml version=\"1.0\"?><hosts><bg>green</bg><msg>FULL</msg>"]
#   rewrite to a host node
	hoststyle = open('host.xsl')
	hostroot = hoststyle.read()
	hoststyle.close()
	hostxslt = ET.XML(hostroot)
	hosttransform = ET.XSLT(hostxslt)
#   just the status color
	statusstyle = open('status.xsl')
	statusroot = statusstyle.read()
	statusstyle.close()
	statusxslt = ET.XML(statusroot)
	statustransform = ET.XSLT(statusxslt)

	doc = open('/usr/share/deez/deezhosts', 'r')
	for line in doc:	
		host = line.strip('\n')
		url = protocol+host+":"+str(port)+path
		try:
			response = http.request('GET', url)
			# checkDeez decides if GREEN or YELLOW
			status = response.data.strip() 
		except Exception as ex:
			# host down or deez out 
			status = "<?xml version=\"1.0\"?><host name=\""+host+"\"><status>RED</status></host>"
		statxml = ET.XML(status)
		color = str(statustransform(statxml))
		if color == "GREEN":
			greendoc.append(str(hosttransform(statxml)))
			green += 1
		elif color == "YELLOW":
			yellowdoc.append(str(hosttransform(statxml)))
			yellow += 1
		elif color == "RED":
			reddoc.append(str(hosttransform(statxml)))
			red += 1
	doc.close()
	reddoc.append("<red>"+str(red)+"</red>"+"<yellow>"+str(yellow)+"</yellow>"+"<green>"+str(green)+"</green>"+"</hosts>")
	yellowdoc.append("<red>"+str(red)+"</red>"+"<yellow>"+str(yellow)+"</yellow>"+"<green>"+str(green)+"</green>"+"</hosts>")
	greendoc.append("<red>"+str(red)+"</red>"+"<yellow>"+str(yellow)+"</yellow>"+"<green>"+str(green)+"</green>"+"</hosts>")
	return([red,"".join(reddoc),yellow,"".join(yellowdoc),green,"".join(greendoc)])

docs = sweepDeez()
if docs[0] > 0:
	bg = "red"
elif docs[2] > 0:
	bg = "yellow"
else:
	bg = "green"

rygdoc = "<?xml version=\"1.0\"?><sums><bg>"+bg+"</bg><red>"+str(docs[0])+"</red><yellow>"+str(docs[2])+"</yellow><green>"+str(docs[4])+"</green></sums>"
rygxml = ET.XML(rygdoc)

rygstyle = open('ryg.xsl')
rygroot = rygstyle.read()
rygstyle.close()
rygxslt = ET.XML(rygroot)
rygtransform = ET.XSLT(rygxslt)
ryghtml = rygtransform(rygxml)
rygfile = open('index.html', 'w+')
rygfile.write(str(ryghtml))
rygfile.close()

hostyle = open('hosts.xsl')
hostsroot = hostyle.read()
hostyle.close()
hostsxslt = ET.XML(hostsroot)
hoststransform = ET.XSLT(hostsxslt)

redhtml = hoststransform(ET.XML(docs[1]))
redfile = open('red.html', 'w+')
redfile.write(str(redhtml))
redfile.close()

yellowhtml = hoststransform(ET.XML(docs[3]))
yellowfile = open('yellow.html', 'w+')
yellowfile.write(str(yellowhtml))
yellowfile.close()

greenhtml = hoststransform(ET.XML(docs[5]))
greenfile = open('green.html', 'w+')
greenfile.write(str(greenhtml))
greenfile.close()
http.clear()
quit()
