#!/usr/bin/python3
# python code for interfacing to VC0706 cameras and grabbing a photo
# https://github.com/adafruit/Adafruit-VC0706-Serial-Camera-Library/blob/master/getimage0706.py
# https://github.com/adafruit/Adafruit_CircuitPython_VC0706/blob/main/adafruit_vc0706.py

import time
import serial
import argparse
from datetime import datetime

s = serial.Serial()

'''
Command format
Protocol sign (1byte) + ID (1byte) + Command (1byte) + Data length (1byte) + Control data (n bytes)

ID: machine identifier. We use "00" as ID in this manual, you should change it according to
real ID of module, you can find it on the surface of module. (important !!!)
'''

COMMANDSEND = 0x56
COMMANDREPLY = 0x76
COMMANDEND = 0x00

CMD_GETVERSION = 0x11
CMD_SETPORT = 0x24
CMD_RESET = 0x26
CMD_FBUF_CTRL = 0x36
CMD_READBUFF = 0x32
CMD_GETBUFFLEN = 0x34
CMD_DOWNSIZE_STATUS = 0x54

VC0706_640x480 = 0x00
VC0706_320x240 = 0x11
VC0706_160x120 = 0x22

VC0706_READ_DATA = 0x30
VC0706_WRITE_DATA = 0x31
VC0706_TV_OUT_CTRL = 0x44
    
def checkreply(r, b):
    if len(r) == 0:
        return False
    if (r[0] == 0x76 and r[1] == s.id and r[2] == b and r[3] == 0x00):
        return True
    return False

'''
RESET Command
<- 56 00 26 00
-> 76 00 26 00 00

After any change, please reset the camera to make the change valid
'''
def reset():
    cmd = bytearray([COMMANDSEND, s.id, CMD_RESET, 0])
    print(cmd.hex())
    s.write(cmd)
    print("Wait ...")
    time.sleep(2)
    reply = s.read(200)
    print(reply.hex())
    if checkreply(reply, CMD_RESET):
        return True
    return False

'''
GET VERSION Command
<- 56 00 11 00
-> 76 00 11 00 0B 56 43 30 37 30 36 20 31 2E 30 30 ("VC0706 1.00")
'''
def getversion():
    cmd = bytearray([COMMANDSEND, s.id, CMD_GETVERSION, 0])
    s.write(cmd)
    reply = s.read(16)
    if len(reply):
        print(reply.decode()[5:])
    if checkreply(reply, CMD_GETVERSION):
        return True
    return False
    
'''
GET SAMPLESIZE command
    READ DATA
    I2C EEPROM：0x56+serial number+0x30+0x04+0x04+the data num ready to read+register address(2 bytes).
    Return format ：
    Ok：0x76+serial number+0x30+0x00+the number of reading+register address
    
<- 56 00 30 04 04 01 00 19
-> 76 00 30 00 01 00
'''
def getsize():
    cmd = bytearray([COMMANDSEND, s.id, VC0706_READ_DATA, 0x04, 0x04, 0x01, 0x00, 0x19])    
    s.write(cmd)
    reply = s.read(6)
    print(reply.hex())
    if checkreply(reply, VC0706_READ_DATA):
        return True
    return False
    
'''
SET SAMPLESIZE command
<- 56 00 31 05 04 01 00 19 P7 (P7-image size 0 for VGA and 0x11 for QVGA)
-> 76 00 31 00 00
'''
def setsize(size):
    cmd = bytearray([COMMANDSEND, s.id, VC0706_WRITE_DATA, 0x05, 0x04, 0x01, 0x00, 0x19, size])
    print(cmd.hex())
    s.write(cmd)
    reply = s.read(5)
    print(reply.hex())
    if checkreply(reply, VC0706_WRITE_DATA):
        return True
    return False


'''
GET COMPRESSRATIO command
<- 56 00 30 04 04 01 00 1a
-> 76 00 30 00 01 35
'''
def getcomression():
    cmd = bytearray([COMMANDSEND, s.id, VC0706_READ_DATA, 0x04, 0x04, 0x01, 0x00, 0x1A])
    s.write(cmd)
    reply = s.read(6)
    print(reply.hex())
    if checkreply(reply, VC0706_READ_DATA):
        return True
    return False
'''
SET COMPRESSRATIO command
<- 56 00 31 05 04 01 00 1A P8 where P8 (1 byte) is the configuration value of image compression ratio.
-> 76 00 31 00 00
'''
def setcomression(ratio):
    cmd = bytearray([COMMANDSEND, s.id, VC0706_WRITE_DATA, 0x05, 0x04, 0x01, 0x00, 0x1A, ratio])
    s.write(cmd)
    reply = s.read(5)
    #print(reply.hex())
    if checkreply(reply, VC0706_WRITE_DATA):
        return True
    return False
'''
TV_OUT_CTRL
    0x56+serial number+0x44+0x01+control item(1 byte)
    0：stop TV output
    1：start TV output
<- 56 00 44 01 00
-> 76 00 44 00 00
'''
def settvout(ctrl):
    cmd = bytearray([COMMANDSEND, s.id, VC0706_TV_OUT_CTRL, 0x01, ctrl])
    s.write(cmd)
    reply = s.read(5)
    print(reply.hex())
    if checkreply(reply, VC0706_TV_OUT_CTRL):
        return True
    return False

'''
SET_PORT command
Set the property of communication interface
<- 56 00 31 05 04 01 00 19 P7 (P7-image size 0 for VGA and 0x11 for QVGA)
-> 76 00 31 00 00
'''
def setport(rate):
    s1relh = 0x2a  # 38400
    s1rell = 0xf2  # 38400
    if rate == 115200:
        s1relh = 0x0d
        s1rell = 0xa6
    cmd = bytearray([COMMANDSEND, s.id, CMD_SETPORT, 0x03, 0x01, s1relh, s1rell])
    print(cmd.hex())
    s.write(cmd)
    reply = s.read(5)
    print(reply.hex())
    if checkreply(reply, CMD_SETPORT):
        return True
    return False


FBUF_STOP_CURRENTFRAME = 0x00
FBUF_STOP_NEXTFRAME = 0x01
FBUF_RESUME_FRAME = 0x02
FBUF_STEP_FRAME = 0x03

'''
FBUF CTRL command
    control flag：
    0：stop current frame
    1：stop next frame
    2：resume frame
    3：step frame

Every stop image capture command will snap an image
    
<- 56 00 36 01 ctrl
-> 76 00 36 00 00
'''
def setfbuf(ctrl):
    cmd = bytearray([COMMANDSEND, s.id, CMD_FBUF_CTRL, 0x01, ctrl])
    print(cmd.hex())
    s.write(cmd)
    reply = s.read(5)
    if len(reply) == 0:
        time.sleep(2)
        print("Timeout! Try again ...")
        reply = s.read(5) # 
    print(reply.hex())
    if checkreply(reply, CMD_FBUF_CTRL) and reply[3] == 0:
        return True
    return False

'''
GET DOWNSIZE STATUS
Command function ： get downsize status
Command format ： 0x56+serial number+0x54+0x00
<- 56 00 54 01 00
-> 76 00 54 00 00
'''
def get_downsize_status():
    cmd = bytearray([COMMANDSEND, s.id, CMD_DOWNSIZE_STATUS, 0x01, 0x00])
    print(cmd.hex())
    s.write(cmd)
    reply = s.read(5)
    print(reply.hex())
    if checkreply(reply, CMD_DOWNSIZE_STATUS):
        return True
    return False

FBUF_TYPE_CURRENTFRAME = 0x00
FBUF_TYPE_NEXTFRAME = 0x01

'''
GET FBUF LEN command

FBUF type：current frame or next frame
0：current frame
1：next frame

<- 56 00 34 01 fbuf_type
-> 76 00 34 00 04 P2 (P2-4 bytes image size)
'''
def getbufferlength(fbuf_type):
    cmd = bytearray([COMMANDSEND, s.id, CMD_GETBUFFLEN, 0x01, fbuf_type])
    print(cmd.hex())
    s.write(cmd)
    r = s.read(10)
    print(r.hex())
    if checkreply(r, CMD_GETBUFFLEN) and r[4] == 0x4:
        l = r[5]
        l <<= 8
        l += r[6]
        l <<= 8
        l += r[7]
        l <<= 8
        l += r[8]
        return l
    return 0

'''
READ FBUF command
The host sends this command to get the image data from frame buffer.
<- 56 00 32 0C 00 0A 00 00 00 00 P3 P4 (P3-4 bytes data size, P4-2 bytes delay)
'''

# inc - bytes to read each time (must be a mutiple of 4)
def readbuffer(fbuf_type, size, inc=1024):

    addr = 0   # the initial offset into the frame buffer
    photo = bytearray()
    readphotocommand = [COMMANDSEND, s.id, CMD_READBUFF, 0x0c, fbuf_type, 0x0a]
    
    while addr < size:
        # on the last read, we may need to read fewer bytes.
        chunk = min(size-addr, inc)

        # append 4 bytes that specify the offset into the frame buffer
        command = readphotocommand + [(addr >> 24) & 0xff, (addr>>16) & 0xff, (addr>>8 ) & 0xff, addr & 0xff]
        # append 4 bytes that specify the data length to read
        command += [(chunk >> 24) & 0xff, (chunk>>16) & 0xff, (chunk>>8 ) & 0xff, chunk & 0xff]
        # append the delay
        # The time unit is 0.01 millisecond
        command += [0x10, 0x00]
        print ("Reading", chunk, "bytes at", addr)
        
        # make a string out of the command bytes.
        cmd = bytearray(command)
        s.write(cmd)

        # the reply is a 5-byte header, followed by the image data
        #   followed by the 5-byte header again.
        r = s.read(5+chunk+5)
        if( len(r) != 5+chunk+5 ):
            # retry the read if we didn't get enough bytes back.
            print ("Read", len(r), "Retrying.")
            continue
        
        if  not checkreply(r, CMD_READBUFF):
            print("ERROR READING PHOTO")
            return False
        
        # append the data between the header data to photo
        photo += r[5:chunk+5]

        # advance the offset into the frame buffer
        addr += chunk
        print("saving" ,addr, "bytes")

    print (addr, "Bytes written")
    return photo
        
def get_current_frame():
    print("Resume Frame")
    setfbuf(FBUF_RESUME_FRAME)
    # <- 5600360102
    # -> 7600360000

    print("Stop current frame")
    if setfbuf(FBUF_STOP_CURRENTFRAME):
        print("--- Snap! ---")
    # <- 5600360100
    # -> 7600360000
    
    print("Get buffer length ")
    return getbufferlength(FBUF_TYPE_CURRENTFRAME)
    # <- 5600340100
    # -> 76003400040000b6b8

        
def get_next_frame():
    print("Step Frame")
    setfbuf(FBUF_STEP_FRAME)
    # <- 5600360103
    # -> 7600360000

    print("Stop next frame")
    if setfbuf(FBUF_STOP_NEXTFRAME):
        print("--- Snap! ---")
    # <- 5600360101
    # -> 7600360000
    
    print("Get buffer length ")    
    return getbufferlength(FBUF_TYPE_NEXTFRAME)
    

def shoot(size=3, inc=1024, next_frame= False):
    
    print("--- Version ---")
    rate_default = s.baudrate
    camera_ok = False
    rate_list = [9600, 19200, 38400, 57600, 115200]
    for rate in rate_list:
        if s.isOpen():
            s.close()
        s.baudrate = rate
        print("Test at", s.baudrate) 
        s.open()
        if not s.isOpen():
            return False
        if getversion():
            print("Camera found at", rate)
            camera_ok = True
            break
            
    if not camera_ok:
        print("Camera not found")
        return False
                
    print("Set port", rate_default)
    if not setport(rate_default):
        return False   
    # <- 56002403010da6
    # -> 7600240000
    
    s.close()
    s.baudrate = rate_default
    s.open()
    if not s.isOpen():
        return False
    
    print("Version")    
    if not getversion():
        return False

    print("Camera found at", s.baudrate)
    
    print("Get size")
    if not getsize():
        return False
        
    print("Get comression ratio")
    if not getcomression():
        return False

    print("Set size", size)
    if size == 0:
        setsize(VC0706_160x120)
    elif size == 1:
        setsize(VC0706_320x240)
    else:
        setsize(VC0706_640x480)    

    print("Set comression ratio")
    setcomression(0x35) # default is 0x35
    
    print("Disable TV out")
    if not settvout(0):
        return False

    print("Get downsize status")
    if not get_downsize_status():
        return False
    # <- 5600540100
    # -> 7600540000

    bytes_to_read = 0
    if next_frame:
        bytes_to_read = get_next_frame()
    else:
        bytes_to_read = get_current_frame()
    print(bytes_to_read, "bytes to read")

    stamp = time.monotonic()
    photo = readbuffer(FBUF_TYPE_NEXTFRAME, bytes_to_read, inc)
    filename = "photo_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

    foldername = "media"
    fullpath = foldername + "/" + filename
    f = open(fullpath, 'wb')
    f.write(photo)
    f.close()
    print("Finished in %0.1f seconds!" % (time.monotonic() - stamp))
    s.close()
    
    return True

def parse_args():
    # Parse input arguments
    desc = 'Interfacing to VC0706 cameras and grabbing a photo'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--port', dest='port',
                        help='port name [/dev/ttyUSB0]',
                        default='/dev/ttyUSB0', type=str)
    parser.add_argument('--baudrate', dest='baudrate',
                        help='port baud rate [38400]',
                        default=38400, type=int)
    parser.add_argument('--size', dest='size',
                        help='image size (0-2) [0]',
                        default=0, type=int)
    parser.add_argument('--timeout', dest='timeout',
                        help='port timeout in seconds [0.5]',
                        default=0.5, type=float)
    parser.add_argument('--chunk', dest='chunk',
                        help='data chunk size (must be multiple of 4) [1024]',
                        default=1024, type=int)
    parser.add_argument('--id', dest='id',
                        help='camera ID [0]',
                        default=0, type=int)    
    parser.add_argument('--next', dest='next_frame',
                        help='use next frame',
                        action="store_true") 
    parser.add_argument('--reset', dest='reset',
                        help='reset camera',
                        action="store_true") 
                        

    args = parser.parse_args()
    return args

if __name__ =="__main__":
    args = parse_args()
    print('Called with args:')
    print(args)
    
    s.baudrate = args.baudrate
    s.timeout = args.timeout
    s.port = args.port
    s.id = args.id  # add id field to serial object!
    
    if args.reset:
        s.open()
        print("Reset")
        reset()
        # <- 56002600
        # -> 76002600 ...
    else:
        if not shoot(args.size, args.chunk, args.next_frame):
            print("--- Error! ---")
