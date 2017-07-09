#!/usr/bin/python
# -*- coding: utf-8 -*-
from tsl256x import Lightsensor
from time import sleep
import time
import twitter
import datetime
from datetime import datetime
import sys
import json

updateInterval = 5.0 * 60.0
currentTime = time.time()

file = open("/home/pi/dev/lightalarm/twitter_tokens.json", "r")
tokens = json.loads(file.read())
file.close()
api = twitter.Api(**tokens)

connectOk = False;
while (connectOk == False):
    try:
        api.PostUpdate("connected" + str(datetime.now()))
        connectOk = True
    except:
        pass


l = Lightsensor()

l.setGain(1)
sleep(1)
lightval = l.getData0()
oldlightval = lightval
status = 0
try:
    while(True):
        
        lightval = l.getData0()
        lightval1 = l.getData1()
        if lightval > 0 and oldlightval > 0:
            ratio = float(lightval1) / float(lightval)
            diff = float(lightval) / float(oldlightval)
    else:
        ratio = 0;
        diff = 0;
        if((diff > 1.5 or lightval > 20) and status == 0):
            sys.stdout.write("läuft; lightval:" + str(lightval) + " diff: " + str(diff) + " ratio:" + str(ratio) + "\n")
            api.PostUpdate("läuft " + str(datetime.now()))
            oldlightval = lightval;
            status = 1
        elif(diff < 0.4 and status == 1):
            sys.stdout.write("fertig; lightval:" + str(lightval) + " diff: " + str(diff) + " ratio:" + str(ratio) + "\n")
            api.PostUpdate("fertig " + str(datetime.now()))
            oldlightval = lightval;
            status = 0
except KeyboardInterrupt:
    print "exit"

