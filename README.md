# BigRedButton

## setup
```
sudo apt-get install libusb-dev mpg123
virtualenv venv
pip install -r requirements.txt
```

## run
Note: since sudo does not preserve shell environment and aliases,
we need to explicitly specify the path to the venv python interpreter
```
sudo venv/bin/python2 buttonDriver.py
```
