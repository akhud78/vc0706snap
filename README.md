# vc0706snap
Python test utility for VC0706 JPG camera

## Requirements
- [TTL Serial Camera](https://learn.adafruit.com/ttl-serial-camera)
- Ubuntu 20.04
- Python 3.8.10
    - [pySerial](https://pyserial.readthedocs.io/en/latest/)
    - [Argparse](https://docs.python.org/3.8/howto/argparse.html#argparse-tutorial)

## Links
- [vc0706_camera](https://github.com/LinuxCircle/vc0706_camera) - LinuxCircle
- [raspi_camera.py](https://github.com/adafruit/Adafruit-VC0706-Serial-Camera-Library/blob/master/raspi_camera.py) - Adafruit TTL JPEG Camera
- [Adafruit CircuitPython VC0706](https://github.com/adafruit/Adafruit_CircuitPython_VC0706)

## Protocol
- [CMOS CAMERA JC425M-Q01](docs/JC425M-Q01_VC0706protocol.pdf) - pdf
- [JPEG Serial Camera Module 0706 Protocol](docs/Manual_0706_Protocol.pdf) - pdf
- [VC0706 protocol](docs/VC0706protocol.pdf) - pdf

## Setup
- Clone and setup [project](https://github.com/akhud78/vc0706snap)

```
$ git clone https://github.com/akhud78/vc0706snap
$ cd vc0706snap
$ mkdir media
```

## Usage
- Help
```
$ python3 vc0706snap.py -h
usage: vc0706snap.py [-h] [--port PORT] [--baudrate BAUDRATE] [--size SIZE]
                     [--timeout TIMEOUT] [--chunk CHUNK] [--id ID] [--next] [--reset]

Interfacing to VC0706 cameras and grabbing a photo

optional arguments:
  -h, --help           show this help message and exit
  --port PORT          port name [/dev/ttyUSB0]
  --baudrate BAUDRATE  port baud rate [38400]
  --size SIZE          image size (0-2) [0]
  --timeout TIMEOUT    port timeout in seconds [0.5]
  --chunk CHUNK        data chunk size (must be multiple of 4) [1024]
  --id ID              camera ID [0]
  --next               use next frame
  --reset              reset camera
```
- Run script
```
$ python3 vc0706snap.py --n
Called with args:
Namespace(baudrate=38400, chunk=1024, id=0, next_frame=True,
          port='/dev/ttyUSB0', reset=False, size=0, timeout=0.5)
--- Version ---
Test at 9600
Test at 19200
Test at 38400
VC0703 1.00
Camera found at 38400
Set port 38400
Version
VC0703 1.00
Camera found at 38400
Get size
Get comression ratio
Set size 0
560031050401001922
Set comression ratio
Disable TV out
Get downsize status
Step Frame
Stop next frame
--- Snap! ---
Get buffer length 
48200 bytes to read
Reading 1024 bytes at 0
saving 1024 bytes
...
Reading 1024 bytes at 47104
saving 48128 bytes
Reading 72 bytes at 48128
saving 48200 bytes
48200 Bytes written
Finished in 17.9 seconds!
```
- View image
```
$ xdg-open media/photo_20220831_155756.jpg
```