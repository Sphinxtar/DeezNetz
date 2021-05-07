#!/usr/bin/python3
# Deez Netz Server Client Sweeper
# reads deezhosts file of one hostname per line
# checks hostname:8142 and gets system status from client
# builds XML tree of statuses in memory 
# applies deezNetz.xsl and writes /var/www/html/deezNetz.js
#	sock.settimeout(8)
import socket
port = 8142
msg = "OK\r\n\r\n"
ok = str.encode(msg)

def sweepDeez():
    doc = open('/usr/share/deez/deezhosts', 'r')
    for line in doc:    
        host = line.strip('\n')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host, 8142))
            sock.sendall(ok)
            while(True):
                data = sock.recv(1024)
                if(data==b''):
                    break
                print(data.decode().strip("\n"))
        except Exception as ex:
            print("<?xml version=\"1.0\"?><host name=\"" +host+"\"><status>RED</status></host>")
            # print(host+":", ex)
        sock.close()
    doc.close()

sweepDeez()
