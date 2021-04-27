# DeezNetz
The Deez Netz Network Monitor

Quickstart: The server has not begun but you can demo the client. 'mkdir /usr/share/deez', copy all three scripts there, 'chmod +x'<br/>
deezyall.py - this installs the service to listen on port 8142<br/>
deezcrawl.py - this gropes your /etc/services, all local web sites and any links in them to build a, 'hostname.xml', file of stuff to scan.<br/>
checkDeez.py - this is the service that scans and gives you the bad news when you connect, you can use socat to test it.<br/>
First run, 'deezyall.py', to create the systemd files and add a line to /etc/services.<br/>
Next run, 'deezcrawl.py', to create the, '/usr/share/deez/hostname.xml', for the service to read. You can edit it for anything you want ignored or added.<br/>
Execute a, 'systemctl enable deeznetz.socket', and, 'systemctl start deeznetz.socket', and you should be ready to rock.<br/>
It will respond with three levels of detail according to the command sent, you can test wtih telnet or:<br/>
'echo OK | socat - 127.0.0.1:8142' will return a simple XML doc of RED or GREEN if something is down or a disk > 85% full.<br/>
'echo ERR | socat - 127.0.0.1:8142' will return a slightly more complex small XML doc detailing just the bad news.<br/>
'echo FULL | socat - 127.0.0.1:8142' will dump everything in knows about the box with current status.<br/>
