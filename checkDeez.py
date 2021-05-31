#!/usr/bin/python3
import socket
import sys
import subprocess
from lxml import etree as ET
import time
import certifi
import urllib3

# The DeezNetz Network Monitor Systemd Service Script
# cmd is how much output to return - OK = red/green - ERR = fails - FULL for everything


url = sys.stdin.readline()
while(True):
	header = sys.stdin.readline()
	if header == "\r\n":
		break

cmd = url.split()[1][1:]

if cmd == "OK":
	report = 0
elif cmd == "ERR":
	report = 1
elif cmd == "FULL":
	report = 2
else:
	sys.stdout.write("HTTP/1.1 404 NOT FOUND\r\n");
	quit()

condition = 0 # 0 = GREEN 1 = RED error condition returned on OK cmd 
stamp = time.asctime(time.gmtime())+" GMT"
docs = "/usr/share/deez/"
hostname = socket.gethostname()
address = socket.gethostbyname(hostname)
file = docs+hostname+'.xml'
https = urllib3.PoolManager(timeout=3.0, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
http = urllib3.PoolManager(timeout=3.0)
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}


def memfree():
	global condition
	highwater = 15; # set this to percentage left to alert on
	fm = (str(subprocess.check_output(["free", "-k"]), 'utf-8')).split('\n')
	freemem = iter(fm)
	next(freemem)
	for row in freemem:
		mlist = row.split()
		break
	free = int(mlist[6])/int(mlist[1])*100
#	print(str(int(mlist[6]))+" / "+str(int(mlist[1]))+"*100="+str(free)+"%")
	if (round(free)<highwater):
		condition = 1
	if report == 2 or (report == 1 and condition == 1):
		retval = "<freemem>"+str(round(free,2))+"%</freemem>"
	else:
		retval = ""
	return(retval)


def diskusage():
	global condition
	highwater = 85 # set this to percentage full to alert on
	diskfull = 0
	retval=[]
	retval.append("<disk>")
	df = (str(subprocess.check_output(["df", "-h"]), 'utf-8')).split('\n')
	dfree = iter(df)
	next(dfree)
	for row in dfree:
		cols = row.split( )
		if len(cols) > 3:
			retval.append("<full>"+cols[0]+" at "+cols[4]+"</full>")
			if int(cols[4].strip('%')) > highwater:
				diskfull = 1
	retval.append("</disk>")
	if diskfull > 0:
		condition = 1
	if report == 0 or (report == 1 and condition != 1):
		return("")
	else:
		return(''.join(retval))


def checkport(port):
	global condition
	retval = "DOWN"
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(8000)
	result = sock.connect_ex((address, port))
	if result == 0:
		retval = "UP"
	else:
		condition = 1
	sock.close()
	return(retval)


# web service see if we get a 200
def checklink(link):
	global condition
	retval = "unknown"
	try:
		if link[0:4].lower() == "https":
			response = https.request('GET',link,fields=None, headers=head)
		else:
			response = http.request('GET',link)	
		if response.status != 200:
			condition = 1
		retval = str(response.status)
	except urllib3.exceptions.ConnectionError:
		retval = "unreachable"
	except urllib3.exceptions.SSLError:
		retval = "bad_ssl_cert"
	except:
		retval = "connect_fail"
	return(retval)


def checkDeez():
	output = []
	outline = []
	down = 0
	first = 1
	output.append("<?xml version=\"1.0\"?><host name=\""+hostname+"\""+" stamp=\""+stamp+"\">")
	tree = ET.parse(file)
	for elem in tree.iter():
		if elem.tag == "host":
			continue

		if elem.tag == "service":
			del outline[:]
			outline.append("<service>")
			down = 0

		if elem.tag == "protocol":
			outline.append("<protocol>"+str(elem.text)+"</protocol>")

		if elem.tag == "url":
			status = checklink(elem.text)
			outline.append("<url err=\""+status+"\">"+str(elem.text)+"</url>")
			if status != "200":
				down = 1

		if elem.tag == "port":
			uprdown = checkport(int(elem.text))
			outline.append("<port status=\""+uprdown+"\">"+str(elem.text)+"</port>")
			if uprdown != "UP":
				down = 1

		if elem.tag == "type":
			outline.append("<type>"+str(elem.text)+"</type></service>")
			if report > 1 or down > 0:
				output.append(''.join(outline))
				del outline[:]
				down = 0


	if report > 0:
		output.append(diskusage())
		output.append(memfree())
	if report == 0:
		del output[:]
		output.append("<?xml version=\"1.0\"?><host name=\""+hostname+"\""+" stamp=\""+stamp+"\">")
		output.append("<status>")
		if condition != 0:
			output.append("YELLOW")
		else:
			output.append("GREEN")
		output.append("</status>")
	if condition == 0 and report == 1:
		output.append("<status>No Errors Found</status>")
	output.append("</host>\r\n")
	del tree
	return(output)


sys.stdout.write("HTTP/1.1 200 OK\r\n");
sys.stdout.write("Connection: keep-alive\r\n" );
sys.stdout.write("Content-Type: text/html; charset=utf-8\r\n" );
sys.stdout.write("Access-Control-Allow-Origin: *\r\n");
msg = ''.join(checkDeez())
if report > 0:
	data = open(docs+'packed.xsl')
	xslt_content = data.read()
	xslt_root = ET.XML(xslt_content)
	dom = ET.fromstring(msg)
	transform = ET.XSLT(xslt_root)
	msg = str(transform(dom))
sys.stdout.write("Content-Length: "+str(len(msg))+"\r\n");
sys.stdout.write("Date: "+time.asctime(time.gmtime())+" GMT\r\n");
sys.stdout.write("\r\n")
sys.stdout.write(msg);
sys.stdout.write("\r\n")
https.clear()
http.clear()
sys.exit(0)
