# Disco Hue

![Alt Text](https://cdn.podnoms.com/fmstuff/stu.gif)

Flash your Hue in time to the groove.

### Installation

Create a virtual env and install the dependencies

```sh
$ virtualenv <env>
$ source <env>/bin/activate
$ pip install -r requirements.txt
$ python disco_hue.py --help
```

### Usage

Create a virtual env and install dependencies

```sh
disco_hue.py [-h] -b BRIDGE_IP [-f FILE] [-l LIGHT_ID]

optional arguments:
  -b BRIDGE_IP, --bridge-ip BRIDGE_IP
                        IP or DNS name of your Hue bridge
  -f FILE, --file FILE  Audio file to play, omit to use currently playing audio (a bit wonky at the moment)
  -l LIGHT_ID, --light-id LIGHT_ID
                        ID of the light you wish to flash (blank to choose interactively)
```
