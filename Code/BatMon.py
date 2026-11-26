#!/usr/bin/env python3
#
# based on ina622 code found here: https://github.com/e71828/pi_ina226/blob/main/example.py
#

import os
import paho.mqtt.publish as publish
import logging
import time
from ina226 import INA226
import configparser
from PIL import ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
import csv
from gpiozero import Button
from gpiozero import OutputDevice

batmonHome = os.path.abspath(os.path.dirname(__file__))
logger = logging.getLogger(__name__)
logging.basicConfig(
                filename=batmonHome + "/batmon.log",
                format="%(asctime)s - %(message)s",
                datefmt="%a, %d %b %Y %H:%M:%S",
                level=logging.INFO,
                )

version = 1.1.0  # Changes shutdown init to long-press of red button.  Short press informs you.

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

redbutton_pin =  26 
leftbutton_pin = 11
midbutton_pin = 12
signalrelay_pin = 25


redbtn = Button(redbutton_pin, pull_up=True, bounce_time=0.05)
leftbtn = Button(leftbutton_pin, pull_up=True, bounce_time=0.05)
midbtn = Button(midbutton_pin, pull_up=True, bounce_time=0.05, hold_time=3)
signal = OutputDevice(signalrelay_pin)

config = configparser.RawConfigParser()
config.read(batmonHome + '/batmon.conf')
mqtt_user = config.get('mqtt','mqtt_user')
mqtt_pass = config.get('mqtt','mqtt_pass')
mqtt_auth = {'username': mqtt_user,'password':mqtt_pass}
font = ImageFont.truetype("DejaVuSans.ttf", 20, encoding="unic")
font2 = ImageFont.truetype("DejaVuSans.ttf", 14, encoding="unic")
pkltoggle = 0
margin = 2
cx = 0
cy = min(device.height, 64) / 2
newfile = ""
run = 1
display = 1
#
##
#
def filecount():
    fc = 0
    plural = "file"
    for root,dir,file in os.walk("/home/greg/BatMon/"):
        fc += len(file)
    if fc > 1:
        plural = "files"
    fc = str(fc)
    return fc,plural
#
## Send an email with the current readings.csv.
#
def msgS(tSub, tMsg, newfile):
    logger.debug("Started msgS() function")
    x = int(config.get("Notify", "NotifyNumber"))
    # tNow = time.strftime("%H:%M:%S", time.localtime())
    for i in range(1, x + 1):
        Email = config.get("Notify", "NotifyEmail" + str(i))
        os.system(
            "echo " + tMsg + " | mail -aFrom:dr.gerg@drgerg.com -A '" + newfile + "' -s " + "'" + tSub + "' " + Email)
#
##  Start a new readings log.
#
def logon():
    global pkltoggle,newfile,display
    display = 0
    pkltoggle = 1
    with canvas(device) as draw:
        draw.text((2 * (cx + margin), cy - 24), "Logging ON", font=font,fill="white")
    newfile = "/home/greg/BatMon/readings " + str(time.strftime("%Y%m%d-%H%M%S", time.localtime())) + ".csv"
    with open(newfile, "w", newline="") as bmr:
        writer = csv.writer(bmr)
        writer.writerow(['Timestamp','Bus_Voltage_V','Bus_Current_mA','Supply_Voltage_V','Shunt_Voltage_mV','Power_mW'])
    time.sleep(1)
    display = 1
#
##  Stop logging readings and email the results.
#
def logoff(ind):
    global pkltoggle,newfile,display
    pkltoggle = 0
    display = 0
    if newfile != "":
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), "Logging OFF", font=font,fill="white")
        with open(newfile, "a", newline="") as bmr:
            writer = csv.writer(bmr)
            writer.writerow(['--==<< End of dataset >>==--','','','','',''])
        time.sleep(1)
        msgS("New BatMon Dataset","Attached is your readings set sent at {}".format(time.strftime("%Y%m%d-%H%M%S", time.localtime())),newfile)
        fc,plural = filecount()
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), "Logging OFF", font=font,fill="white")
            draw.text((2 * (cx + margin), cy), fc + " " + plural + ".", font=font2, fill="white")
        newfile = ""
    time.sleep(1)
    if ind == 0:
        display = 1
#
##  MIDDLE BUTTON: Single press Toggles Logging.  If toggling off, emails results.
##                  Long-press cleans old logs out of ~/BatMon/ .
#
def m_press():
    global pkltoggle,newfile,display
    midbtn.wait_for_release(2)
    if midbtn.is_pressed == 0:
        if pkltoggle == 0:
            logon()
        else:
            logoff(0)
    if midbtn.is_pressed == 1:
        display = 0
        if pkltoggle == 1:
            logoff(0)
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), "Cleaning", font=font,fill="white")
        os.system('rm /home/greg/BatMon/*')
        fc,plural = filecount()
        time.sleep(1)
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), "Cleaned", font=font,fill="white")
            draw.text((2 * (cx + margin), cy), fc + " in ~/BatMon.", font=font2, fill="white")
        time.sleep(2)
        display = 1
#
##  LEFT BUTTON: Single press flags current log showing a new start point.
#
def l_press():
    global pkltoggle,newfile,display
    display = 0
    if pkltoggle == 1:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        with open(newfile, "a", newline="") as bmr:
            writer = csv.writer(bmr)
            writer.writerow(['--==<< Restart Testing >>==--','','','','',''])
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), "Flagged New Tests", font=font2,fill="white")
            draw.text((2 * (cx + margin), cy), timestamp, font=font2,fill="white")
        time.sleep(2)
        display = 1
    else:
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), "No log active.", font=font2,fill="white")
        time.sleep(2)
        display = 1

#
##  RIGHT (RED) BUTTON: Long-press starts the Pi's shutdown process.
#
def r_press():
    global display,redpress,timer,timefp
    display = 0
    redbtn.wait_for_release(2)
    if redbtn.is_pressed == 0:
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), "Press/Hold", font=font,fill="white")
            draw.text((2 * (cx + margin), cy), "to pwr down.", font=font,fill="white")
        time.sleep(2)
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), " Returning", font=font,fill="white")
            draw.text((2 * (cx + margin), cy), " to work.", font=font,fill="white")
        display = 1
    if redbtn.is_pressed == 1:
        display = 0
        with canvas(device) as draw:
            draw.text((2 * (cx + margin), cy - 24), " Remove", font=font,fill="white")
            draw.text((2 * (cx + margin), cy), " Power", font=font,fill="white")
        logoff(1)
        time.sleep(1)
        os.system("echo 'endit' > ShutDownNow")

#
## Bind the callback functions
#
redbtn.when_pressed = r_press
leftbtn.when_pressed = l_press
midbtn.when_pressed = m_press

def getPwrReadings():
    readings = {'BV':ina.voltage(),'BA':ina.current(),'SV':ina.supply_voltage(),'ShV':ina.shunt_voltage(),'W':ina.power()}
    if readings['BA'] < 100.0:
        signal.on()
    if readings['BA'] > 100.0:
        signal.off()
    return readings

def stdoutreadings(readings):
    global pkltoggle,newfile,display
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    if display == 1:
        if pkltoggle == 1:
            ptd = "Log on"
        if pkltoggle == 0:
            ptd = "Log off"
        with canvas(device) as draw:
            suppv = str("%.2f" % readings['BV'])
            loadma = str("%.2f" % readings['BA'])
            draw.text((2 * (cx + margin), cy - 24), "Bus Volts : " + suppv, font=font2,fill="white")
            draw.text((2 * (cx + margin), cy), "Bus Load | " + ptd + "\n" + loadma + "mA    ", font=font2, fill="white")
    if pkltoggle == 1:
        if os.path.isfile(newfile):
            with open(newfile, "a", newline="") as bmr:
                writer = csv.writer(bmr)
                writer.writerow([timestamp,readings['BV'],readings['BA'],readings['SV'],readings['ShV'],readings['W']])

def outwardComm(readings):
    #
    ## SEND STUFF TO MQTT SERVER
    #
    # logger.info("outwardComm: sensor: {}, tempC: {}, tempF2: {}, humid: {}\ntemps: {}.".format(sensor,tempC,tempF2,humid,temps))
    publish.single("batmon/state/bus_voltage", readings['BV'], auth=mqtt_auth, hostname="192.168.30.150")
    publish.single("batmon/state/bus_current_ma", readings['BA'], auth=mqtt_auth, hostname="192.168.30.150")
    publish.single("batmon/state/supply_voltage", readings['SV'], auth=mqtt_auth, hostname="192.168.30.150")
    publish.single("batmon/state/shunt_voltage", readings['ShV'], auth=mqtt_auth, hostname="192.168.30.150")
    publish.single("batmon/state/power_mw", readings['W'], auth=mqtt_auth, hostname="192.168.30.150")
    #

def main():
    global run
    while run == 1:
        ina.wake(3)
        # time.sleep(3)
        while run == 1:
            if ina.is_conversion_ready():
                # time.sleep(3)
                readings = getPwrReadings()
                stdoutreadings(readings)
                outwardComm(readings)
                break
        time.sleep(1)

ina = INA226(busnum=1, max_expected_amps=20, log_level=logging.INFO)
ina.configure()
ina.set_low_battery(5)
with canvas(device) as draw:
    draw.text((2 * (cx + margin), cy - 24), "  BATMON  ", font=font,fill="white")
    draw.text((2 * (cx + margin), cy), "     by drgerg", font=font2, fill="white")
time.sleep(3)
with canvas(device) as draw:
    draw.text((2 * (cx + margin), cy - 24), "Flag | Togl | ShDn", font=font2,fill="white")
    draw.text((2 * (cx + margin), cy), "        | DEL |     ", font=font2, fill="white")
time.sleep(5)
fc,plural = filecount()
with canvas(device) as draw:
    draw.text((2 * (cx + margin), cy - 24), "~/BatMon files", font=font2,fill="white")
    draw.text((2 * (cx + margin), cy), "quantity: " + fc, font=font2, fill="white")
time.sleep(3)
readings = getPwrReadings()
stdoutreadings(readings)
outwardComm(readings)
time.sleep(2)
ina.wake(3)
time.sleep(0.2)
main()

    
