import logging
import os

from dotenv import load_dotenv
import nfc


def on_connect(tag: nfc.tag.Tag) -> bool:
    print("connected")

    with open('dump_result.txt', 'w') as f:
        f.write("\n".join(tag.dump()))

    # Trueを返しておくとタグが存在しなくなるまで待機される
    return True

def on_release(tag: nfc.tag.Tag) -> None:
    print("released")


if __name__ == "__main__":
    load_dotenv()
    BUS_NO    = int(os.getenv('PASORI_BUS_NO'))
    DEVICE_NO = int(os.getenv('PASORI_DEVICE_NO'))
    
    logging.basicConfig(level=logging.DEBUG)

    # lsusbコマンドでBus No.とDevice No.を確認する
    path = f"usb:{BUS_NO:03}:{DEVICE_NO:03}"
    with nfc.ContactlessFrontend(path) as clf:
        clf.connect(
            rdwr={
                "on-connect": on_connect,
                "on-release": on_release
            }
        )
