# DeezNetz
The Deez Netz Network Monitor
Better Living With XML/XSLT

Quickstart: The server has not begun but you can demo the client. 'mkdir /usr/share/deez', copy all three scripts there, 'chmod +x' and set the executable bit on all of them.<br/>
deezyall.py - this will install the service to listen on port 8142, creates two service files in /lib/systemd/system and a line in /etc/services for you.<br/>
deezcrawl.py - this gropes your /etc/services, all local web sites and any links in them to build a, 'hostname.xml', file of stuff to scan. If your hostname is set to localhost and you have your services to monitor on an external interface you can change it and then change it back afterwards and rename the file, edit name= attrib in first tag at the top.<br/>
checkDeez.py - This is the service that scans and gives you the bad news when you connect, you can use socat to test it.<br/>
First run, 'deezyall.py', to create the systemd files and add a line to /etc/services.<br/>
Next run, 'deezcrawl.py', to create the, '/usr/share/deez/hostname.xml', for the service to read. You can edit it for anything you want ignored or added, like web services with invalid certificates or paths that won't resolve<br/>
Execute, 'systemctl enable deeznetz.socket', and, 'systemctl start deeznetz.socket', and a, 'systemctl daemon-reload', and it should be listening and ready.<br/>
You can control it all by the socket file, 'systemctl status deeznetz.socket', should show you everything it's up to.
It will respond with three levels of detail according to the command sent, you can test it with socat:<br/>
'echo OK |socat - TCP4:127.0.0.1:8142' will return a simple XML doc of RED or GREEN if something is down or a disk > 85% full.<br/>
'echo ERR |socat - TCP4:127.0.0.1:8142' will return a slightly more complex small XML doc detailing just the bad news.<br/>
'echo FULL |socat - TCP4:127.0.0.1:8142' will dump everything in knows about the box with current status.<br/>
Still working on the Network Monitor Central Command Console to utilize this on every host. All suggestions welcome. Current thought is leaning toward a Java servlet in Tomcat ui.<br/>
