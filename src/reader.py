import os
from typing import cast

from dotenv import load_dotenv
import nfc
from nfc.tag import Tag
from nfc.tag.tt3 import BlockCode
from nfc.tag.tt3 import ServiceCode
from nfc.tag.tt3 import Type3Tag
from nfc.tag.tt3_sony import FelicaStandard

from auth import check_student_id
from lock import LockController


lock_ctrler = LockController()

class FeliCaReader:
    # lsusbコマンドで調べる
    BUS_NO    = 3
    DEVICE_NO = 6

    def __init__(self) -> None:
        load_dotenv()

        # System
        self.SYSTEM_CODE = int(os.getenv('SYSTEM_CODE'), 16)
        # Service
        self.SERVICE_NO   = int(os.getenv('SERVICE_NO'))
        self.SERVICE_ATTR = int(os.getenv('SERVICE_ATTR'), 16)
        # Block
        self.BLOCK_NO = int(os.getenv('BLOCK_NO'))

    def read(self):
        path = f'usb:{self.BUS_NO:03}:{self.DEVICE_NO:03}'
        with nfc.ContactlessFrontend(path) as clf:
            clf.connect(
                rdwr={
                    'on-connect': self.on_connect,
                    'on-release': self.on_release
                }
            )

    def on_connect(self, tag: Tag) -> bool:
        print('connected')

        #　FeliCaのカードである
        if isinstance(tag, FelicaStandard):
            system_code = tag.request_system_code()
            # 所望のシステムコードが存在する
            if self.SYSTEM_CODE in system_code:
                tag.idm, tag.pmm, *_ = tag.polling(self.SYSTEM_CODE)

                # 学生番号を取得する
                student_id = self.get_student_id(tag)
                # print(student_id)

                # 研究室の学生であった場合
                if check_student_id(student_id):
                    # ロックの状態を変更する
                    lock_ctrler.switch_lock_status()

        # Trueを返しておくとタグが存在しなくなるまで待機される
        return True
    
    def get_student_id(self, tag: Type3Tag) -> str:
        student_id_bytearr = self.read_data_block(tag)
        student_id_block = student_id_bytearr.decode('shift_jis')

        return student_id_block[0:8]

    def read_data_block(self, tag: Type3Tag) -> bytearray:
        service_code = ServiceCode(self.SERVICE_NO, self.SERVICE_ATTR)
        block_code = BlockCode(self.BLOCK_NO)
        data_block = (
            cast(
                bytearray,
                tag.read_without_encryption(
                    [service_code],
                    [block_code]
                )
            )
        )

        return data_block
    
    def on_release(self, tag: Tag) -> None:
        print('released')


if __name__ == '__main__':
    reader = FeliCaReader()
    reader.read()
