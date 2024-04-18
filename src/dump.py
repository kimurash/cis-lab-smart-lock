import logging

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
    logging.basicConfig(level=logging.DEBUG)

    with nfc.ContactlessFrontend(f"usb:003:006") as clf:
        clf.connect(
            rdwr={
                "on-connect": on_connect,
                "on-release": on_release
            }
        )

