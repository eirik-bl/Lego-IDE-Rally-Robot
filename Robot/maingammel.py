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

sweep=15
swing_speed=50
tid1=3
tid2=5

(red, green, blue) = colorSensor.rgb()
is_black=True
funnet_svart=False
ev3.speaker.set_volume(100)

def finn_strek(): #få en sjekk for om den er på innsiden eller utsiden av linja, slik at den vet hvilken vei den skal starte å svinge
    global red, green, blue, is_black, SVART
    global sweep
    global swing_speed
    global funnet_svart
    funnet_svart = False
    robot.drive(0,-sweep)
    while not funnet_svart:
        if sweep>180:
            robot.drive(0,-sweep)
            sweep=15
        
        start_time=time.time()
        end_time = time.time()+tid1
        print(start_time,end_time)
        while end_time > time.time():
            (red, green, blue) = colorSensor.rgb()
            print("første loop")
            is_black = red < RED and green < GREEN and blue < BLUE
            print("rød: ",red)
            print("grønn: ",green)
            print("blå: ",blue)
            print("black?: ",is_black)
            if is_black:
                print("is black første loop")
                robot.stop()
                funnet_svart=True
                return
        

        print("nå har jeg stoppet")
        robot.drive(0,sweep*2)
        start_time=time.time()
        end_time = time.time()+tid2

        print(start_time,end_time)
        while end_time  > time.time():
            (red, green, blue) = colorSensor.rgb()
            is_black = red < RED and green < GREEN and blue < BLUE
            if is_black:
                print("is black andre loop")
                robot.stop()
                funnet_svart=True
                return

        #sving tilbake til midten, ellers drar roboten seg bare én vei
        #-sweep + 2*sweep - sweep = 0, så den ender der den startet
        #robot.drive(0,-sweep)

        sweep+=15
        # legg til counter her og når den er for mye ha if statement under is blakc for å sjekke andre vei


def forover_vanlig():
    global red, green, blue, is_black, SVART
    global funnet_svart
    robot.drive(250,0)
    while is_black:
        if US_sensor.distance() <= 75:
            ev3.speaker.play_file(SoundFile.CHEERING)
            return True
        is_black = red < RED and green < GREEN and blue < BLUE
        (red, green, blue) = colorSensor.rgb()
        SVART = round(((300-(red + green + blue))/3),3)
        print("mengde svart: ", SVART)
        #print("rød: ",red)
        #print("grønn: ",green)
        #print("blå: ",blue)
        print("black?: ",is_black)
            
        if not is_black:
            robot.stop()
            funnet_svart=False
            return


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
    hindring=forover_vanlig()
    if hindring:
        ev3.speaker.say("Wall found!") #gjør noe her hvis ønsket
    wait(10)
    finn_strek()
