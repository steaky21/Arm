import usb.core, usb.util, cwiid, time
while (Arm == None):
    Arm = usb.core.find(idVendor=0x1267, idProduct=0x0000)
def ArmMove(Duration, ArmCmd):
    Arm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 1000)
time.sleep(1)
ArmCmd=[0,0,0]
Arm.ctrl_transfer(0x40, 6, 0x100, 0, ArmCmd, 1000)
Wii = None
while (Wii==None):
    try:
        Wii = cwiid.Wiimote()
    except: RuntimeError:
        print 'Error connecting to the Wiimote, press 1 and 2 '
