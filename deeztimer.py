#!/usr/bin/python3
# DeezNetz Server Service Timer Installer
# Writes The DeezNetz Systemd Timer and Service Files

def createServiceFile():
    sysdeez = open('/lib/systemd/system/sweepDeez.service', 'w+')
    sysdeez.write('[Unit]\n')
    sysdeez.write('Description=DeezNetz Sweep Service\n')
    sysdeez.write('Wants=sweepDeez.timer\n\n');
    sysdeez.write('[Service]\n')
    sysdeez.write('Type=oneshot\n')
    sysdeez.write('ExecStart=-/usr/share/deez/sweepDeez.py\n\n')
    sysdeez.write('[Install]\n')
    sysdeez.write('WantedBy=multi-user.target\n\n')
    sysdeez.close()
    print('New /lib/systemd/system/sweepDeez.service file written.')

def createTimerFile():
    timerdeez = open('/lib/systemd/system/sweepDeez.timer', 'w+')
    timerdeez.write('[Unit]\n')
    timerdeez.write('Description=DeezNetz Sweep Timer\n')
    timerdeez.write('Requires=sweepDeez.service\n\n')
    timerdeez.write('[Timer]\n')
    timerdeez.write('Unit=sweepDeez.service\n')
    timerdeez.write('OnCalendar=*:0/5:0\n')
    timerdeez.write('[Install]\n')
    timerdeez.write('WantedBy=timers.target\n\n')
    timerdeez.close()
    print('New /lib/systemd/system/sweepDeez.timer file written.')


createServiceFile()
createTimerFile()

