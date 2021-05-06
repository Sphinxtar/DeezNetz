#!/usr/bin/python3
# Deez Netz Server Client Sweeper
# reads deezhosts file of one hostname per line
# checks hostname:8142 and gets system status from client
# builds XML tree of statuses in memory 
# applies deezNetz.xsl and writes /var/www/html/deezNetz.js
import socket

def sweepDeez():
	port = 8142
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(8)
	doc = open('/usr/share/deez/deezhosts', 'r')
	for line in doc:    
		host = line.strip('\n')
		print(host)
		addr = socket.getaddrinfo(host, None, socket.AF_INET)
		print(addr[1][4][0])
		result = sock.connect_ex((addr[1][4][0], port))
		if result == 0:
			print("connected to "+host, port)
			sock.send("OK".encode())
			statstr = sock.recv(256)
			print(statstr.decode())
		else:
			print("connection failed to "+host, port)
	sock.close()
	doc.close()


sweepDeez()
