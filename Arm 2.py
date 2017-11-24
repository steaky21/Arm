import usb.core, usb.util, cwiid, time

#Give our robot arm an easy name so that we only need to specify all the junk required for the usb connection once
print ('Make sure the arm is ready to go.')
print ('')
Armc = 1750
Arm  = None
while (Arm == None):
    #This connects to the usb
    Arm = usb.core.find(idVendor=0x1267, idProduct=0x0000)
    #This will wait for a second, and then if the program could not connect, it tells us and tries again
    Armc = Armc + 1
    if (Armc == 2000):
        print ('Could not connect to Arm, double check its connections.')
        print ('Program will continue when connection is established...')
        print ('')
        Armc = Armc/2000
        continue

#Set up our arm transfer protocol through the usb and define a Value we can change to control the arm
Duration = 1
ArmLight = 0

#Create delay variable that we can use (Seconds)
Delay = .1
Counter = 9999
def ArmMove(Duration, ArmCmd):

    #Start Movement
    Arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)
    time.sleep(Duration)

    #Stop Movement
    ArmCmd=[0,0,ArmLight]
    Arm.ctrl_transfer(0x40,6,0x100,0,ArmCmd,1000)

#Establish a connection with the wiimote
print ('Connected to arm successfully.')
print ('')
print ('Press 1 and 2 on the wiimote at the same time.')
#Connect to mote and if it doesn't connect then it tells us and tries again
time.sleep(3)
print ('')
print ('Establishing Connection... 5')
time.sleep(1)
print ('Establishing Connection... 4')
time.sleep(1)
print ('Establishing Connection... 3')
Wii = None
while (Wii==None):
    try:
        Wii = cwiid.Wiimote()
    except RuntimeError:
        print ('Error connecting to the wiimote, press 1 and 2.')
print ('Establishing Connection... 2')
time.sleep(1)
print ('Establishing Connection... 1')
time.sleep(1)
print ('')

#Once a connection has been established with the two devices the rest of the program will continue; otherwise, it will keep on trying to connect to the two devices

#Rumble to indicate connection and turn on the LED
Wii.rumble = 1 #1 = on, 0 = off
print ('Connection Established.')
print ('Press any button to continue...')
print ('')

''' Each number turns on different leds on the wiimote
    ex) if Wii.led = 1, then LED 1 is on
    2  = LED 2          3  = LED 3          4  = LED 4
    5  = LED 1, 3       6  = LED 2, 3       7  = LED 1,2,3
    8  = LED 4          9  = LED 1, 4       10 = LED 2,4
    11 = LED 1,2,4      12 = LED 3,4        13 = LED 1,3,4
    14 = LED 2,3,4      15 = LED 1,2,3,4
    It counts up in binary to 15'''
time.sleep(1)
Wii.rumble = 0
Wii.led = 15

# Set it so that we can tell when and what buttons are pushed, and make it so that the accelerometer input can be read
Wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC | cwiid.RPT_EXT
Wii.state

while True:

    #This deals with the accelerometer
    '''create a variable containing the x accelerometer value
    (changes if mote is turned or flicked left or right)
    flat or upside down = 120, if turned: 90 degrees cc = 95, 90 degrees c = 145'''
    Accx = (Wii.state['acc'][cwiid.X])

    '''create a variable containing the y accelerometer value
    (changes when mote is pointed or flicked up or down)
    flat = 120, IR pointing up = 95, IR pointing down = 145'''
    Accy = (Wii.state['acc'][cwiid.Y])

    '''create a variable containing the z accelerometer value
    (Changes with the motes rotation, or when pulled back or flicked up/down)
    flat = 145, 90 degrees cc or c, or 90 degrees up and down = 120, upside down = 95'''
    Accz = (Wii.state['acc'][cwiid.Z])


    #This deals with the buttons, we tell every button what we want it to do
    buttons = Wii.state['buttons']
    #Get battery life (as a percent of 100):
    #Just delete the nunber sign inn front
    #print Wii.state['battery']*100/cwiid.BATTERY_MAX

    # If the home button is pressed then rumble and quit, plus close program
    if (buttons & cwiid.BTN_HOME):
        print ('')
        print ('Closing Connection...')
        ArmLight = 0
        ArmMove(.1,[0,0,0])
        Wii.rumble = 1
        time.sleep(.5)
        Wii.rumble = 0
        Wii.led = 0
        exit(Wii)

    ''' Arm Commands Defined by ArmMove are
    [0,1,0]   Rotate Base Clockwise
    [0,2,0]   Rotate Base C-Clockwise
    [64,0,0]  Shoulder Up
    [128,0,0] Shoulder Down
    [16,0,0]  Elbow Up
    [32,0,0]  Elbow Down
    [4,0,0]   Wrist Up
    [8,0,0]   Wrist Down
    [2,0,0]   Grip Open
    [1,0,0]   Grip Close
    [0,0,1]   Light On
    [0,0,0]   Light Off

    ex) ArmMove(Duration in seconds,[0,0,0])
    This example would stop all movement and turn off the LED'''

    #Check to see if other buttons are pressed
    if (buttons & cwiid.BTN_A):
        print ('A pressed')
        time.sleep(Delay)
        ArmMove(.1,[1,0,ArmLight])
    if (buttons & cwiid.BTN_B):
        print ('B pressed')
        time.sleep(Delay)
        ArmMove(.1,[2,0,ArmLight])
    if (buttons & cwiid.BTN_1):
        print ('1 pressed')
        ArmMove(.1,[16,0,ArmLight])
    if (buttons & cwiid.BTN_2):
        (print '2 pressed')
        ArmMove(.1,[32,0,ArmLight])
    if (buttons & cwiid.BTN_MINUS):
        print ('Minus pressed')
        ArmMove(.1,[8,0,ArmLight])
    if (buttons & cwiid.BTN_PLUS):
        print ('Plus pressed')
        ArmMove(.1,[4,0,ArmLight])
    if (buttons & cwiid.BTN_UP):
        print ('Up pressed')
        ArmMove(.1,[64,0,ArmLight])
    if (buttons & cwiid.BTN_DOWN):
        print ('Down pressed')
        ArmMove(.1,[128,0,ArmLight])
    if (buttons & cwiid.BTN_LEFT):
        print ('Left pressed')
        ArmMove(.1,[0,2,ArmLight])
    if (buttons & cwiid.BTN_RIGHT):
        print ('Right pressed')
        ArmMove(.1,[0,1,ArmLight])

    #Here we handle the nunchuk, along with the joystick and the buttons
    while(1):
        if Wii.state.has_key('nunchuk'):
            try:
                #Here is the data for the nunchuk stick:
                #X axis:LeftMax = 25, Middle = 125, RightMax = 225
                NunchukStickX = (Wii.state['nunchuk']['stick'][cwiid.X])
                #Y axis:DownMax = 30, Middle = 125, UpMax = 225
                NunchukStickY = (Wii.state['nunchuk']['stick'][cwiid.Y])
                #The 'NunchukStickX' and the 'NunchukStickY' variables now store the stick values

                #Here we take care of all of our data for the accelerometer
                #The nunchuk has an accelerometer that records in a similar manner to the wiimote, but the number range is different
                #The X range is: 70 if tilted 90 degrees to the left and 175 if tilted 90 degrees to the right
                NAccx = Wii.state['nunchuk']['acc'][cwiid.X]
                #The Y range is: 70 if tilted 90 degrees down (the buttons pointing down), and 175 if tilted 90 degrees up (buttons pointing up)
                NAccy = Wii.state['nunchuk']['acc'][cwiid.Y]
                #I still don't understand the z axis completely (on the wiimote and nunchuk), but as far as I can tell it's main change comes from directly pulling up the mote without tilting it
                NAccz = Wii.state['nunchuk']['acc'][cwiid.Z]

                #Make it so that we can control the arm with the joystick
                if (NunchukStickX < 60):
                    ArmMove(.1,[0,2,ArmLight])
                    print ('Moving Left')
                if (NunchukStickX > 190):
                    ArmMove(.1,[0,1,ArmLight])
                    print ('Moving Right')
                if (NunchukStickY < 60):
                    ArmMove(.1,[128,0,ArmLight])
                    print ('Moving Down')
                if (NunchukStickY > 190):
                    ArmMove(.1,[64,0,ArmLight])
                    print ('Moving Up')

#Make it so that we can control the arm with tilt Functions
                #Left to Right
                if (Accx < 100 and NAccx < 90 ):
                    ArmMove(.1,[0,2,ArmLight])
                    print ('Moving Left')
                if (Accx > 135 and NAccx > 150):
                    ArmMove(.1,[0,1,ArmLight])
                    print ('Moving Right')

                #Up and Down
                if (Accy < 100 and NAccy < 90):
                    ArmMove(.1,[64,0,0])
                    print ('Moving Up')
                if (Accy > 135 and NAccy > 150):
                    ArmMove(.1,[128,0,0])
                    print ('Moving Down')

                #Here we create a variable to store the nunchuck button data
                #0 = no buttons pressed
                #1 = Z is pressed
                #2 = C is pressed
                #3 = Both C and Z are pressed

                ChukBtn = Wii.state['nunchuk']['buttons']
                if (ChukBtn == 1):
                    print ('Z pressed')
                    ArmLight = 0
                    ArmMove(.1,[0,0,ArmLight])
                if (ChukBtn == 2):
                    print ('C pressed')
                    ArmLight = 1
                    ArmMove(.1,[0,0,ArmLight])
                #If both are pressed the led blinks
                if (ChukBtn == 3):
                    print ('C and Z pressed')
                    ArmMove(.1,[0,0,0])
                    time.sleep(.25)
                    ArmMove(.1,[0,0,1])
                    time.sleep(.25)
                    ArmMove(.1,[0,0,0])
                    time.sleep(.25)
                    ArmMove(.1,[0,0,1])
                    time.sleep(.25)
                    ArmMove(.1,[0,0,0])
                    time.sleep(.25)
                    ArmMove(.1,[0,0,1])
                    time.sleep(.25)
                    ArmMove(.1,[0,0,0])

                #Any other actions that require the use of the nunchuk in any way must be put here for the error handling to function properly
                break

#This part down below is the part that tells us if no nunchuk is connected to the wiimote
            except KeyError:
                print ('No nunchuk detected!')
        else:
            if (ArmLight == 0):
                if (Accz > 179 or Accz < 50):
                    ArmLight = 1
                    ArmMove(.1,[0,0,ArmLight])
                    time.sleep(.5)
            elif (ArmLight == 1):
                if (Accz > 179 or Accz < 50):
                    ArmLight = 0
                    ArmMove(.1,[0,0,ArmLight])
                    time.sleep(.5)

            if (Counter == 10000):
                print ('No nunchuk detected!')
                Counter = Counter/10000
                break
            Counter = Counter + 1
            break
