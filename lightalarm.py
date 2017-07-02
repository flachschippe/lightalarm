#!/usr/bin/python
# -*- coding: utf-8 -*-
from tsl256x import Lightsensor
from time import sleep
import twitter
import datetime
from datetime import datetime
import sys
import json

file = open("/home/pi/dev/lightalarm/twitter_tokens.json", "r")
tokens = json.loads(file.read())
file.close()
api = twitter.Api(**tokens)

connectOk = False;
while (connectOk == False):
    try:
        api.PostUpdate("Connect ok " + str(datetime.now()))
        connectOk = True
    except:
        pass


l = Lightsensor()

l.setGain(1)
sleep(1)
lightval = l.getData0();
oldlightval = lightval;
status = 0
try:
    while(True):
        
        lightval = l.getData0();
        ratio = float(l.getData1 ()) / lightval;

        diff = float(lightval) / float(oldlightval)
        if((diff > 1.5 or lightval > 100) and status == 0):
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

