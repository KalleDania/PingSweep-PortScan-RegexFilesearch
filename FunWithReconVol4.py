import os, socket, re, sys, threading, time
from subprocess import Popen, DEVNULL

def getPingSweep():
    print("Ping sweeping from OS: " + str(sys.platform))
    if "win" in sys.platform :
        osSpecificFlag = "-c"
    elif "linux" in sys.platform :
        osSpecificFlag = "-n"  
    p = {} # ip -> process    
    for i in range(254):
        cBlock = i
        for j in range(254):
            dBlock = j
            ip = "192.168." + str(cBlock) + "." + str(dBlock)
            p[ip] = Popen(['ping', osSpecificFlag, '-w5', '-c3', ip], stdout=DEVNULL)
        while p:
            for ip, proc in p.items():
                if proc.poll() is not None: # ping finished
                    del p[ip] # remove from the process list
                    if proc.returncode == 0:
                        print('%s active' % ip)
                        activeIps.append(ip)
                    elif proc.returncode == 1:
                        #print('%s no response' % ip)
                        pass
                    else:
                        #print('%s error' % ip)
                        pass
                    break             
    print(str(len(activeIps)) + " hosts were alive: ")
    for k in range(len(activeIps)):
        print(activeIps[k])

def doPortscanOn(_activeIPs):
    openPorts = []
    for i in range(len(_activeIPs)):
        for port in range(1,1024):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                sock.connect((_activeIPs[i],port))
                openPorts.append((_activeIPs[i] + " ",port))
                print (_activeIPs[i] + " " + str(port) + " OPEN")
            except Exception as exception:
                #print(_activeIPs[i] + " " + str(port) + " " + str(exception))
                pass
            sock.close()
    for k in range(len(openPorts)):
        print(openPorts[k])

def lookForInterestingFiles():
    interestingFiles = []
    rootsToCheck = []
    if "win" in sys.platform :
        rootsToCheck.append("c:\\")
    elif "linux" in sys.platform :
        rootsToCheck += ["/root/", "/home/"]
    else:
        print("OS: " + str(sys.platform) + " is not Windows or Linux, cant scan for files..")
        return
    for k in range(len(rootsToCheck)):	
        print("Scanning OS: " + str(sys.platform) + " root: " + rootsToCheck[k])
        try:
            for path, dirnames, filenames in os.walk(rootsToCheck[k]):
                for j in range(len(filenames)):
                    #I have reason to suspect the format of the flagname is something like this:
                    if re.match('(^\d_\d.(jpg|png|gif|bmp)$)', str(filenames[j]).lower()) or \
                        "password" in str(filenames[j]).lower() or \
                        "login" in str(filenames[j]).lower() or \
                        "alice" in str(filenames[j]).lower() or \
                        "peter" in str(filenames[j]).lower() or \
                        "copenhagen" in str(filenames[j]).lower() or \
                        "bank" in str(filenames[j]).lower() or \
                        "privat" in str(filenames[j]).lower():
                         fileAndPathToAdd = str(filenames[j]), " ", path
                         interestingFiles.append(fileAndPathToAdd)
        except Exception as exception:
            print("Exception: " + str(exception))
    print("-------DONE. PRINTING FILENAMES AND PATHS-------------")
    for i in range(len(interestingFiles)):
        print(interestingFiles[i])

print("-------PING SWEEP-----------------------------------")
activeIps = []
getPingSweep()
print("-------PORT SCAN WITH SOCKETS-----------------------")
doPortscanOn(activeIps)
print("-------FILEHUNTING WITH REGEX-----------------------")
lookForInterestingFiles()

wait = input("Press to exit...")
