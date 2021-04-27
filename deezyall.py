#!/usr/bin/python3
# DeezNetz Client Installation Installer
# Creates The DeezNetz Client Service

def addServiceLine():
    found = False;
    svcs = open('/etc/services', 'r+')
    for line in svcs:
        line = line.strip('\n')
        words = line.split()
        if (len(words) > 0 and words[0] == 'deeznetz' and words[1] == '8142/tcp'):
            found = True
            print("Serice deeznetz 8142/tcp already in /etc/services.")
            break
    if (found == False):
        print("Adding deeznetz 8142/tcp to /etc/services.")
        svcs.write('deeznetz        8142/tcp                # DeezNetz Network Monitor\n')
    svcs.close()

def createServiceFile():
    sysdeez = open('/lib/systemd/system/deeznetz@.service', 'w+')
    sysdeez.write('[Unit]\n')
    sysdeez.write('Description=DeezNetz Network Monitor\n')
    sysdeez.write('After=network.target deeznetz.socket\n')
    sysdeez.write('Requires=deeznetz.socket\n\n')
    sysdeez.write('[Service]\n')
    sysdeez.write('Type=oneshot\n')
    sysdeez.write('ExecStart=-/usr/share/deez/checkDeez.py\n')
    sysdeez.write('StandardInput=socket\n')
    sysdeez.write('RemainAfterExit=yes\n\n')
    sysdeez.write('[Install]\n')
    sysdeez.write('WantedBy=multi-user.target\n')
    sysdeez.close()
    print('New /lib/systemd/system/deeznetz@.service file written.')

def createSocketFile():
    sockdeez = open('/lib/systemd/system/deeznetz.socket', 'w+')
    sockdeez.write('[Unit]\n')
    sockdeez.write('Description=DeezNetz Network Monitor Socket\n')
    sockdeez.write('PartOf=deeznetz@.service\n\n')
    sockdeez.write('[Socket]\n')
    sockdeez.write('ListenStream=8142\n')
    sockdeez.write('Accept=Yes\n\n')
    sockdeez.write('[Install]\n')
    sockdeez.write('WantedBy=multi-user.target\n')
    sockdeez.close()
    print('New /lib/systemd/system/deeznetz.socket file written.')


addServiceLine()
createServiceFile()
createSocketFile()

