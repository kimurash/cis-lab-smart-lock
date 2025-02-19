import os
import sys

from dotenv import load_dotenv
import usb.core
import usb.util


def detach_kernel_driver():
    VENDOR_ID  = int(os.getenv("PASORI_VENDOR_ID"), 16)
    PRODUCT_ID = int(os.getenv("PASORI_PRODUCT_ID"), 16)

    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if device is None:
        sys.exit("device not found")

    if device.is_kernel_driver_active(0):
        try:
            device.detach_kernel_driver(0)
            print("kernel driver detached")
        except usb.core.USBError as err:
            sys.exit(err)


if __name__ == "__main__":
    load_dotenv()
    detach_kernel_driver()
