#!/usr/bin/python3
# crawl the sockets on a box and create an XML file for DeezNetz
# dive into any http/https ports and add nodes for all the URL's found
import sys
import datetime
import certifi
import urllib3
import socket
from bs4 import BeautifulSoup

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

# can change next line to CERT_NONE to skip them
https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
http = urllib3.PoolManager()
web  = ['http','https']
name = socket.gethostname()
hrefs = []

def checkservice(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(8)
    result = sock.connect_ex((ip, port))
    if result == 0:
        return(True)
    else:
        return(False)
    sock.close()


# web service so recursively probe and add any links
def probe(site, xdoc):
	try:
		if site[0:4].lower() == "https":
			apage = https.request('GET', site, fields=None, headers=head)
		else:
			apage = http.request('GET', site, fields=None, headers=head)
			apage = http.request('GET', site)
		xdoc.write("<url err=\""+str(apage.status)+"\">"+site+"</url>")
		soup = BeautifulSoup(apage.data, features="lxml")
		links = soup.find_all("a")
		for link in links:
			if link.get("href") not in hrefs and link.get("href") != site:
				hrefs.append(link.get("href"))
			probe(link.get("href"),0)
	except urllib3.exceptions.ConnectionError:
		xdoc.write("<url err=\"unreachable\">"+site+"</url>")
		return
	except urllib3.exceptions.InsecureRequestWarning:
		xdoc.write("<url err=\"TLSV13_ALERT_CERTIFICATE_REQUIRED)\">"+site+"</url>")
	except:
		return
	return


def buildXMLconfig(host):
    addr = socket.gethostbyname(host)
    doc = open('/usr/share/deez/' + host + '.xml', 'w')
    doc.write("<host>")
    svcs = open('/etc/services', 'r')
    for line in svcs:
        line = line.strip('\n')
        words = line.split()
        if (len(words) > 0 and words[0][0] != '#'):
            port = words[1].split('/')
            if checkservice(addr, int(port[0])):
                doc.write("<service>")
                doc.write("<protocol>" + words[0] + "</protocol>")
                if words[0] in web:
                    probe(words[0] + "://" + host + "/", doc)
                doc.write("<port status=\"UP\">" + port[0] + "</port>")
                doc.write("<type>" + port[1] + "</type>")
                doc.write("</service>")
    svcs.close()
    doc.write("</host>\n")
    doc.close()


buildXMLconfig(name)
http.clear()
https.clear()
