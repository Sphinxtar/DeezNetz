#!/usr/bin/python3
import socket
import sys
import subprocess
import xml.etree.ElementTree as ET
import datetime
import requests

# The DeezNetz Network Monitor Systemd Service Script
# cmd is how much output to return - OK returns red/green - ERR returns only the fails in english - FULL for whole XML doc

cmd = sys.stdin.readline().strip().upper()
if cmd == "OK":
    report = 0
elif cmd == "ERR":
    report = 1
else:
    report = 2
condition = 0 # 0 = GREEN 1 = RED error condition returned on OK cmd 
stamp = datetime.datetime.now().replace(microsecond=0).isoformat()
docs = "/usr/share/deez/"
hostname = socket.gethostname()
address = socket.gethostbyname(hostname)
file = docs+hostname+'.xml'

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
    global condition
    retval = "unknown"
    try:
        apage = requests.get(link,timeout=4.0)
        if apage.status_code != 200:
            condition = 1
        retval = str(apage.status_code)
    except requests.exceptions.ConnectionError:
        retval = "unreachable"
    return(retval)


def checkDeez():
    firstserve = 0
    sys.stdout.write("<?xml version=\"1.0\"?><host name=\""+ hostname + "\">")
    tree = ET.parse(file)
    for elem in tree.iter():
        if elem.tag == "host":
            continue

        if elem.tag == "service":
            if firstserve == 0: 
                if report > 1:
                    sys.stdout.write("<service>")
                firstserve=1
            else:
                if report > 1:
                    sys.stdout.write("</service><service>")
            continue

        if elem.tag == "url":
            status = checklink(elem.text)
            if report > 0:
                if (status != "200" and report > 0) or report == 2:
                    sys.stdout.write("<url err=\""+status+"\">"+str(elem.text)+"</url>")
            continue

        if elem.tag == "port":
            uprdown = checkport(int(elem.text))
            if (uprdown != "UP" and report > 0) or report == 2:
                sys.stdout.write("<port status=\""+uprdown+"\">"+str(elem.text)+"</port>")
            continue

        if elem.tag == "check":
            if report > 1:
                sys.stdout.write("<"+str(elem.tag)+">"+stamp+"</"+str(elem.tag)+">")
            continue

        if elem.text != "None":
            if report > 1:
                sys.stdout.write("<"+str(elem.tag)+">"+str(elem.text)+"</"+str(elem.tag)+">")
            continue
        else:
            if report > 1:
                sys.stdout.write("<"+str(elem.tag)+">")

    if report > 1:
        sys.stdout.write("</service>")
    sys.stdout.write(diskusage())
    if report == 0:
        sys.stdout.write("<status>")
        if condition != 0:
            sys.stdout.write("RED")
        else:
            sys.stdout.write("GREEN")
        sys.stdout.write("</status>")
    if condition == 0 and report == 1:
        sys.stdout.write("<status>No Errors Found</status>")
    sys.stdout.write("</host>\r\n")
    del tree

checkDeez()
sys.exit(0)
