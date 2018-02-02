# phue sample

Show and update Philips hue.

## env
Python 3.6.3

## setup

1. Install python packages via pip.

```sh
$ virtualenv venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

2. Connect your HomeBridge and phone in the same LAN.
3. Setup Hue App on your phone and find IP of HomeBridge.

## Run

### demo

```sh
(venv) $ python hue.py demo --ip [HomeBridge_IP] -i [light_id]
```

### show current value

```sh
(venv) $ python hue.py show --ip [HomeBridge_IP] -i [light_id]
```

### update value

```sh
(venv) $ python hue.py set --ip [HomeBridge_IP] -i [light_id] --bri [0-255] --color-rgb-hex [rrggbb]
```

### Turn off

```sh
(venv) $ python hue.py set --ip [HomeBridge_IP] -i [light_id] --off
```


### help

```sh
(venv) $ python hue.py --help
```
