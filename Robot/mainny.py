#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import time
import random
from threading import Thread

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


'''
OPPGAVEBESKRIVELSE:


'''


# Create your objects here.
ev3 = EV3Brick()


# Definerer delene
motor1 = Motor(Port.A,Direction.COUNTERCLOCKWISE,gears=None)#port, positiv direction, gears=None
motor2 = Motor(Port.C,Direction.COUNTERCLOCKWISE,gears=None) # ^^
robot = DriveBase(motor2,motor1,wheel_diameter=56,axle_track=116) #definerer roboten som klassen DriveBase()
US_sensor = UltrasonicSensor(Port.S2)
colorSensor = ColorSensor(Port.S4)



RED=30
GREEN=30
BLUE=80 #Juster etter testing om for sensetiv
SVART=0

sweep=20 #hvor langt den søker første gang (grader)
sweep_okning=20 #hvor mye lenger den søker hver gang den snur
sweep_maks=120 #søker aldri lenger enn dette til hver side
steg=8 #grader per lille sving, lavere = mindre sjanse for å hoppe over streken
swing_speed=250 #grader/s i robot.turn(), brukes mest i de store hoppene tilbake
sving_akselerasjon=2000 #grader/s², høyere = hvert steg går fortere
fart=250 #mm/s rett fram

#setter bare svingfart og svingakselerasjon, beholder resten av standardinnstillingene
(s_speed, s_acc, t_rate, t_acc) = robot.settings()
robot.settings(s_speed, s_acc, swing_speed, sving_akselerasjon)

(red, green, blue) = colorSensor.rgb()
is_black=True
funnet_svart=False
sist_retning=-1 #-1 = venstre, 1 = høyre. Søker først den veien den fant streken sist
ev3.speaker.set_volume(100)

def sjekk_svart():
    global red, green, blue, is_black
    (red, green, blue) = colorSensor.rgb()
    is_black = red < RED and green < GREEN and blue < BLUE
    return is_black

def finn_strek(): #svinger i små steg og sjekker sensoren etter hvert steg, fram og tilbake med større og større utslag
    global funnet_svart, sist_retning
    funnet_svart = False
    retning = sist_retning
    vinkel = 0 #hvor langt den har svingt fra der den mistet streken
    grense = sweep #lokal, så søket starter smått hver gang
    sokt_venstre = 0 #hvor langt til venstre den allerede har sjekket (negativ vinkel)
    sokt_hoyre = 0 #hvor langt til høyre den allerede har sjekket
    while not funnet_svart:
        #hopper raskt i én sving over området den allerede vet er hvitt
        kjent = sokt_venstre if retning < 0 else sokt_hoyre
        if vinkel != kjent:
            robot.turn(kjent - vinkel)
            vinkel = kjent

        while vinkel*retning < grense:
            robot.turn(retning*steg) #turn() bremser selv når den er ferdig, så den sklir ikke forbi
            vinkel += retning*steg
            if sjekk_svart():
                funnet_svart=True
                sist_retning=retning
                return

        if retning < 0:
            sokt_venstre = vinkel
        else:
            sokt_hoyre = vinkel

        #har sjekket helt ut på begge sider uten å finne noe: begynn på nytt fra midten
        if -sokt_venstre >= sweep_maks and sokt_hoyre >= sweep_maks:
            sokt_venstre = 0
            sokt_hoyre = 0

        retning = -retning #snu og let andre vei
        grense = min(grense + sweep_okning, sweep_maks)


def forover_vanlig():
    global funnet_svart
    robot.drive(fart,0)
    while sjekk_svart():
        pass

    robot.stop()
    funnet_svart=False


ev3.speaker.beep()

'''
def threaded(func):
    def wrapper(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
        return t
    return wrapper

play_sound_file = threaded(sound.play_file)      # ev3dev2
say_text = threaded(ev3.speaker.say)              # Pybricks
'''


while True:
    forover_vanlig()
    finn_strek()
