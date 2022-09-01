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
usage: vc0706snap.py [-h] [--port PORT] [--resolution RESOLUTION]
                      [--timeout TIMEOUT] [--chunk CHUNK]

Interfacing to VC0706 cameras and grabbing a photo

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           device name [/dev/ttyUSB0]
  --resolution RESOLUTION
                        image resolution (0-2) [0]
  --timeout TIMEOUT     port timeout in seconds [0.5]
  --chunk CHUNK         data chunk size (must be multiple of 4) [1024]
```
- Run script
```
$ python3 vc0706snap.py --r 0 --c 512
Called with args:
Namespace(chunk=512, port='/dev/ttyUSB0', resolution=0, timeout=0.5)
--- Version ---
VC0703 1.00
Camera found
Set Size
Reset
--- Snap! ---
2856 bytes to read
Reading 512 bytes at 0
saving 512 bytes
Reading 512 bytes at 512
saving 1024 bytes
Reading 512 bytes at 1024
saving 1536 bytes
Reading 512 bytes at 1536
saving 2048 bytes
Reading 512 bytes at 2048
saving 2560 bytes
Reading 296 bytes at 2560
saving 2856 bytes
2856 Bytes written
Finished in 1.4 seconds!
```
- View image
```
$ xdg-open media/photo_20220831_155756.jpg
```