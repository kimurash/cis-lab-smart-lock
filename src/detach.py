import os
import sys

from dotenv import load_dotenv
import usb.core
import usb.util


def detach_kernel_driver():
    vendor_id  = os.getenv("VENDOR_ID")
    product_id = os.getenv("PRODUCT_ID")

    device = usb.core.find(idVendor=vendor_id, idProduct=product_id)
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
