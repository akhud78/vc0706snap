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
usage: vc0706snap.py [-h] [--port PORT] [--baudrate BAUDRATE] [--resolution RESOLUTION] 
       [--timeout TIMEOUT] [--chunk CHUNK] [--id ID]

Interfacing to VC0706 cameras and grabbing a photo

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           port name [/dev/ttyUSB0]
  --baudrate BAUDRATE   port baud rate [38400]
  --resolution RESOLUTION
                        image resolution (0-2) [0]
  --timeout TIMEOUT     port timeout in seconds [0.5]
  --chunk CHUNK         data chunk size (must be multiple of 4) [1024]
  --id ID               camera ID [0]
```
- Run script
```
$ python3 vc0706snap.py --p /dev/ttyUSB1 --r 0 --c 1024 --id 1
Called with args:
Namespace(baudrate=38400, chunk=1024, id=1, port='/dev/ttyUSB1', resolution=0, timeout=0.5)
--- Version ---
VC0706 1.99
Camera found
Set size
Set comression ratio
Reset
Take photo
--- Snap! ---
29554 bytes to read
Reading 1024 bytes at 0
saving 1024 bytes
Reading 1024 bytes at 1024
saving 2048 bytes
...
Reading 882 bytes at 28672
saving 29554 bytes
29554 Bytes written
Finished in 8.2 seconds!
```
- View image
```
$ xdg-open media/photo_20220831_155756.jpg
```