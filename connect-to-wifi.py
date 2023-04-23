import pywifi
import subprocess
from os import system
from time import sleep


wifi = pywifi.PyWiFi()

interfaces = wifi.interfaces()

for i in interfaces:
    print(str(interfaces.index(i)) + " >> " + i.name())

if len(interfaces) == 1:
    interfaceindex = 0
else:
    arg = input("select interface index or Enter for DEFULTE (index0)\n")
    interfaceindex = int(arg)


interface = interfaces[interfaceindex]

def scan():
    interface.scan()
    print("SCANNING",end="")
    while pywifi.const.IFACE_SCANNING == interface.status():
        print(".",end="")

    
    avas = interface.scan_results()
    for v in avas:
        print(str(avas.index(v)) + " >> " + v.ssid)
        
    return avas[int(input("select availble network index\n"))].ssid

    


def set_profile(ssid):    
    networks = subprocess.check_output(["netsh", "wlan", "show", "networks"]).decode("utf-8").splitlines()
    for net in networks:
        if ssid in net:
            index = networks.index(net)
            print(net)
            conf = [
            networks[index+1].replace("    Network type            : ",""),
            networks[index+2].replace("    Authentication          : ",""),
            networks[index+3].replace("    Encryption              : ",""),
            ]
            
            

    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    if "WPA2-Personal" in conf[1]:
        profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    if "CCMP" in conf[2]:
        profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
    profile.key = input("pass > ")

    interface.add_network_profile(profile)
    return profile



if pywifi.const.IFACE_DISCONNECTED == interface.status():
    print("DISCONNECTED")

elif pywifi.const.IFACE_SCANNING == interface.status():
    print("SCANNING",end="")
    while pywifi.const.IFACE_SCANNING == interface.status():
        print(".",end="")
    print("\n")

elif pywifi.const.IFACE_INACTIVE == interface.status():
    print("INACTIVE")
elif pywifi.const.IFACE_CONNECTING == interface.status():

    print("CONNECTING")
    while pywifi.const.IFACE_CONNECTING == interface.status():
        print(".",end="")
    print("\n")

elif pywifi.const.IFACE_CONNECTED == interface.status():
    print("CONNECTED")
    interface.disconnect()

ssid = scan()
profile = set_profile(ssid=ssid)

interface.connect(profile)




print(f"CONNECTING {ssid}",end="")
while pywifi.const.IFACE_CONNECTED != interface.status():
    print(".",end="")
    sleep(1)
    

    
print(f"\nCONNECTED {ssid}")