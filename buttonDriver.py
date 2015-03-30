#!/usr/bin/python
from usb import core, util
import atexit
from time import sleep
from array import array

'''
Extensive credit goes to https://gist.github.com/arr2036/9932438

I basically copied his c driver into python.  I was able to figure out
what variables he chose for bmRequestType, but not why- and there were
a bunch of settings that I have no idea why they work.  Fun stuff either
way!  This requires libusb to be installed (I tested with v 1.0).  It
also will not work on OSX.  OSX kernel claims the device as a HID, and
the function to force the kernal to release HID devices has not yet
been written for libusb (and is apparently difficult).
'''

VENDOR_ID = 7476
PRODUCT_ID = 13
POLL_INTERVAL = .1

BUTTON_STATE_ERROR = -1
BUTTON_STATE_UNKNOWN = 0
BUTTON_STATE_LID_CLOSED = 0x15
BUTTON_STATE_PRESSED = 0x16
BUTTON_STATE_LID_OPEN = 0x17

should_exit = False
kernel_was_attached = False

def get_device_handle():
    dev = core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        raise SystemError("Device not found!")

    interface = 0  # HID

    # Free red button from kernel driver
    # This does not work on OSX
    if dev.is_kernel_driver_active(interface) is True:
        dev.detach_kernel_driver(interface)
        util.claim_interface(dev, interface)
        kernel_was_attached = True

    return dev


def set_button_control(dev):

    # Transfer control to the button HID interface
    bm_request_type = util.build_request_type(
        util.CTRL_OUT,
        util.CTRL_TYPE_CLASS,
        util.CTRL_RECIPIENT_INTERFACE
    )

    state = array('B', [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02])
    ret = dev.ctrl_transfer(bm_request_type, 0x09, 0x00, 0x00, state)
    if ret < 0:
        print "Error reading control response"
        return -1
    if ret == 0:
        print "Device didn't sent enough data"
        return -1

    return 0


def read_button_state(dev):
    if set_button_control(dev) < 0:
        return -1
    endpoint = dev[0][(0, 0)][0]  # Interrupt IN
    try:
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize, timeout=2000)
    except:
        return -1
    return data[0]


def cleanup():
    print "Cleaning up"
    interface = 0
    # release the device
    util.release_interface(device_handle, interface)
    # reattach the device to the OS kernel
    device_handle.attach_kernel_driver(interface)


def button_pressed():
    print "BAM"


def button_not_pressed():
    pass


def lid_opened():
    print "WARNING..."

command = {
    BUTTON_STATE_LID_CLOSED: button_not_pressed,
    BUTTON_STATE_PRESSED: button_pressed,
    BUTTON_STATE_LID_OPEN: lid_opened
}

atexit.register(cleanup)

then = BUTTON_STATE_UNKNOWN

device_handle = get_device_handle()
if read_button_state(device_handle) == BUTTON_STATE_ERROR:
    exit()

while True:
    now = read_button_state(device_handle)
    if now == BUTTON_STATE_ERROR:
        sleep(POLL_INTERVAL)
        continue
    if then == now:
        sleep(POLL_INTERVAL)
        continue
    if then == BUTTON_STATE_PRESSED:
        # Released action - no op
        then = now
        continue
    command[now]()
    then = now
