# vc0706-test
python 3 test for vc7060 camera

## Requirements
- Ubuntu 20.04
- Python 3

## Links
- [vc0706_camera](https://github.com/LinuxCircle/vc0706_camera) - LinuxCircle
- [raspi_camera.py](https://github.com/adafruit/Adafruit-VC0706-Serial-Camera-Library/blob/master/raspi_camera.py) - Adafruit TTL JPEG Camer
- [Adafruit CircuitPython VC0706](https://github.com/adafruit/Adafruit_CircuitPython_VC0706)

## Building
- Clone and setup [project](https://github.com/akhud78/vc0706-test)

```
$ git clone https://github.com/akhud78/vc0706-test
$ cd vc0706-test
$ mkdir media
```

## Usage
- Run script
```
$ python3 vc0706_test.py 
760011000b56433037303320312e3030
VC0703 1.00
VC0706 Camera found
7600310000
7600360000
Snap!
760034000400000e38
3640 bytes to read
Reading 3640 bytes at 0
saving 3640 bytes
3640 Bytes written
```
- View image
```
$ xdg-open media/photo_20220831_155756.jpg
```