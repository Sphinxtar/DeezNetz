#!/usr/bin/python3
# Deez Netz Server Client Sweeper
# reads deezhosts file of one hostname per line
# checks hostname:8142 and gets system status from client
# builds XML tree of statuses in memory 
# applies deezNetz.xsl and writes /var/www/html/deezNetz.js
#		sock.settimeout(8)
import socket
from lxml import etree as ET

port = 8142
msg = "OK\r\n\r\n"
ok = str.encode(msg)


def sweepDeez():
	status = []
	xmldoc = ["<?xml version=\"1.0\"?><hosts>"]
	hoststyle = open('hostdoc.xsl')
	hostroot = hoststyle.read()
	hoststyle.close()
	hostxslt = ET.XML(hostroot)
	hosttransform = ET.XSLT(hostxslt)

	doc = open('/usr/share/deez/deezhosts', 'r')
	for line in doc:    
		host = line.strip('\n')
		status.clear()
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((host, 8142))
			sock.sendall(ok)
			while(True):
				data = sock.recv(1024)
				if(data==b''):
					break
				else:
					status.append( data.decode().strip("\n"))
		except Exception as ex:
			status.append("<?xml version=\"1.0\"?><host name=\"" +host+"\"><status>RED</status></host>")
		sock.close()
		statii = ''.join(status)
		statxml = ET.XML(statii)
		xmldoc.append(str(hosttransform(statxml)))

	doc.close()
	xmldoc.append("</hosts>")
	return("".join(xmldoc))

print(sweepDeez())
