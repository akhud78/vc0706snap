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
CMD_RESET = 0x26
CMD_TAKEPHOTO = 0x36
CMD_READBUFF = 0x32
CMD_GETBUFFLEN = 0x34

FBUF_CURRENTFRAME = 0x00
FBUF_NEXTFRAME = 0x01

FBUF_STOPCURRENTFRAME = 0x00

VC0706_640x480=0x00
VC0706_320x240=0x11
VC0706_160x120=0x22

VC0706_READ_DATA=0x30
VC0706_WRITE_DATA=0x31

    
def checkreply(r, b):
    if (r[0] == 0x76 and r[1] == s.id and r[2] == b and r[3] == 0x00):
        return True
    return False

'''
RESET Command
<- 56 00 26 00
-> 76 00 26 00 00
'''
def reset():
    cmd = bytearray([COMMANDSEND, s.id, CMD_RESET, 0])
    s.write(cmd)
    reply = s.read(100)
    #print(replay.hex())
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
    #print(reply.hex())
    print(reply.decode()[5:])
    if checkreply(reply, CMD_GETVERSION):
        return True
    return False
'''
SET SAMPLESIZE command
<- 56 00 31 05 04 01 00 19 P7 (P7-image size 0 for VGA and 0x11 for QVGA)
-> 76 00 31 00 00
'''
def setsize(size):
    cmd = bytearray([COMMANDSEND, s.id, VC0706_WRITE_DATA, 0x05, 0x04, 0x01, 0x00, 0x19, size])
    s.write(cmd)
    reply = s.read(5)
    #print(reply.hex())
    if checkreply(reply, VC0706_WRITE_DATA):
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
FBUF CTRL command
<- 56 00 36 01 P1 (0-Stop frame buffer data update at current frame, 3-Resume normal video state)
-> 76 00 36 00 00
'''
def takephoto():
    cmd = bytearray([COMMANDSEND, s.id, CMD_TAKEPHOTO, 0x01, FBUF_STOPCURRENTFRAME])
    s.write(cmd)
    reply = s.read(5)
    if len(reply) == 0:
        time.sleep(2)
        print("Timeout! Try again ...")
        reply = s.read(5) # 
    #print(reply.hex())
    if checkreply(reply, CMD_TAKEPHOTO) and reply[3] == 0:
        return True
    return False

'''
GET FBUF LEN command
<- 56 00 34 01 00
-> 76 00 34 00 04 P2 (P2-4 bytes image size)
'''
def getbufferlength():
    cmd = bytearray([COMMANDSEND, s.id, CMD_GETBUFFLEN, 0x01, FBUF_CURRENTFRAME])
    s.write(cmd)
    r = s.read(10)
    #print(r.hex())
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
def readbuffer(size, inc=1024):

    addr = 0   # the initial offset into the frame buffer
    photo = bytearray()
    readphotocommand = [COMMANDSEND, s.id, CMD_READBUFF, 0x0c, FBUF_CURRENTFRAME, 0x0a]
    
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
        

def shoot(resolution=3, inc=1024):
    print("--- Version ---")
    if (not getversion()):
        print("Camera not found")
        exit(0)
    print("Camera found")

    print("Set size")
    if resolution == 0:
        setsize(VC0706_160x120)
    elif resolution == 1:
        setsize(VC0706_320x240)
    else:
        setsize(VC0706_640x480)    

    print("Set comression ratio")
    setcomression(0x35) # default is 0x35

    print("Reset")
    reset()

    print("Take photo")
    if takephoto():
        print("--- Snap! ---")
        
    bytes_to_read = getbufferlength()
    print(bytes_to_read, "bytes to read")
    
    stamp = time.monotonic()
    photo = readbuffer(bytes_to_read, inc)
    filename = "photo_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"

    foldername = "media"
    fullpath = foldername + "/" + filename
    f = open(fullpath, 'wb')
    f.write(photo)
    f.close()
    print("Finished in %0.1f seconds!" % (time.monotonic() - stamp))
    
    return fullpath

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
    parser.add_argument('--resolution', dest='resolution',
                        help='image resolution (0-2) [0]',
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
    
    s.open()
    if s.isOpen():
        shoot(args.resolution, args.chunk)
    s.close()
