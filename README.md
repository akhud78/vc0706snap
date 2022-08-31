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
/dev/ttyUSB0 38400 0.5
--- Version ---
VC0703 1.00
Camera found
Set Size
Reset
Snap!
42556 bytes to read
Reading 1024 bytes at 0
saving 1024 bytes
Reading 1024 bytes at 1024
...
Reading 1024 bytes at 40960
saving 41984 bytes
Reading 572 bytes at 41984
saving 42556 bytes
42556 Bytes written
Finished in 15.8 seconds!
```
- View image
```
$ xdg-open media/photo_20220831_155756.jpg
```