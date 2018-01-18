# phue sample

## env
Python 3.6.3

## setup
1. Install python packages via pip.
```
$ virtualenv venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

2. Config python_hue.json
Make `python_hue.json` from `python_hue.json.sample`.
Enter HomeBridge IP address.

## Run
```
(venv) $ python hue.py
```
