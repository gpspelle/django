# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import network
import usocket
import utime
import ujson
from ntptime import settime
from machine import Timer

# Get list of known WiFi networks
try :
    with open('/networks.json', 'r') as netfile :
        knownnets = ujson.load(netfile)
except :
    knownnets = {}

netprio = list(knownnets.keys())
netprio.sort()

if len(netprio) > 0 :
    print("Trying to connect to a known WiFi network")
    # Firstly, try to connect to a known WiFi network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()
    # Get the SSIDs of the networks
    netnames = [n[0].decode('utf-8') for n in networks]
    for net in netprio :
        if net < 0 :
            continue
        ssid = knownnets[net]['ssid']
        if ssid in netnames :
            print("Trying to connect to", ssid)
            wlan.connect(ssid, knownnets[net]['pword'])
            utime.sleep(5)  # Wait 5 seconds for the connection
            if wlan.isconnected() :
                print("Success!")
                break
            print("Failure.")

    print("Trying to create a WiFi network")
    # Secondly, if no network was found, create our own
    if not wlan.isconnected() :

        led_r = Pin(22, Pin.OUT)
        led_r.value(1)
        wlan.active(False)
        for net in netprio :
            if net >= 0 :
                continue
            wlan = network.WLAN(network.AP_IF)
            wlan.active(True)
            wlan.config(essid=knownnets[net]['ssid'], password=knownnets[net]['pword'])

    # Print our IP address and the network we are on
    print(wlan.ifconfig()[0], " on ", wlan.config('essid'))

# If we can reach an NTP server, setup a timer to fix the drift of the RTC every hour
if len(usocket.getaddrinfo('pool.ntp.org', 123)) > 0 :
    # Setup a timer to set the time from pool.ntp.org
    ntp_timer = Timer(-1)
    ntp_timer.init(period=3600000, mode=Timer.PERIODIC, callback=lambda t:settime())
    settime()
