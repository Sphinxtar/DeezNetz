#!/usr/bin/python3
import socket
import sys
import subprocess
import xml.etree.ElementTree as ET
import time
import requests
import urllib3
# comment out the next line to enable insecure SSL Certificate warnings
# make sure your certificates are all up to date first
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
validateSSL = False # True will validate bad/self signed certificates

def diskusage():
    global condition
    highwater = 85 # set this to percentage full to alert on
    diskfull = 0
    retval = "<disk>"
    df = (str(subprocess.check_output(["df", "-h"]), 'utf-8')).split('\n')
    dfree = iter(df)
    next(dfree)
    for row in dfree:
        cols = row.split( )
        if len(cols) > 3:
            if int(cols[4].strip('%')) > highwater:
                retval = retval + "<full>"+cols[0]+" at "+cols[4]+"</full>"
                diskfull = 1
    retval = retval + "</disk>"
    if diskfull > 0:
        condition = 1
    if report == 0 or condition != 1:
        retval = ""
    return(retval)


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
    global validateSSL
    global condition
    retval = "unknown"
    try:
        apage = requests.get(link,timeout=4.0,verify=validateSSL)
        if apage.status_code != 200:
            condition = 1
        retval = str(apage.status_code)
    except requests.exceptions.ConnectionError:
        retval = "unreachable"
    except requests.exceptions.SSLError:
        retval = "bad_ssl_cert"
    return(retval)


def checkDeez():
    output=[]
    firstserve = 0
    output.append("<?xml version=\"1.0\"?><host name=\""+hostname+"\""+" stamp=\""+stamp+"\">")
    tree = ET.parse(file)
    for elem in tree.iter():
        if elem.tag == "host":
            continue

        if elem.tag == "service":
            if firstserve == 0: 
                if report > 1:
                    output.append("<service>")
                firstserve=1
            else:
                if report > 1:
                    output.append("</service><service>")
            continue

        if elem.tag == "url":
            status = checklink(elem.text)
            if report > 0:
                if (status != "200" and report > 0) or report == 2:
                    output.append("<url err=\""+status+"\">"+str(elem.text)+"</url>")
            continue

        if elem.tag == "port":
            uprdown = checkport(int(elem.text))
            if (uprdown != "UP" and report > 0) or report == 2:
                output.append("<port status=\""+uprdown+"\">"+str(elem.text)+"</port>")
            continue

        if elem.text != "None":
            if report > 1:
                output.append("<"+str(elem.tag)+">"+str(elem.text)+"</"+str(elem.tag)+">")
            continue
        else:
            if report > 1:
                output.append("<"+str(elem.tag)+">")

    if report > 1:
        output.append("</service>")
    output.append(diskusage())
    if report == 0:
        output.append("<status>")
        if condition != 0:
            output.append("RED")
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
sys.stdout.write("Content-Length: "+str(len(msg))+"\r\n");
sys.stdout.write("Date: "+time.asctime(time.gmtime())+" GMT\r\n");
sys.stdout.write("\r\n")
sys.stdout.write(msg);
sys.stdout.write("\r\n")
sys.exit(0)
