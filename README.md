# BigRedButton

## setup
```
sudo apt-get install -y python-virtualenv libusb-dev mpg123
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## run
Note: since sudo does not preserve shell environment and aliases,
we need to explicitly specify the path to the venv python interpreter
```
source venv/bin/activate
sudo venv/bin/python buttonDriver.py
```
