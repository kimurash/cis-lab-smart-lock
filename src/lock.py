import base64
import hashlib
import hmac
import os
import time
import uuid

from dotenv import load_dotenv
import requests


class LockController:
    host_domain = 'https://api.switch-bot.com'

    def __init__(self) -> None:
        load_dotenv()
        self.token  = os.getenv('SWITCHBOT_TOKEN')
        self.secret = os.getenv('SWITCHBOT_SECRET')

        self.get_device_id()

    def make_api_header(self):
        # Declare empty header dictionary
        api_header = {}

        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(self.token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        # Build api header JSON
        api_header['Authorization'] = self.token
        api_header['Content-Type'] = 'application/json'
        api_header['charset'] = 'utf8'
        api_header['t'] = str(t)
        api_header['sign'] = str(sign, 'utf-8')
        api_header['nonce'] = str(nonce)

        return api_header

    def get_device_id(self):
        api_header = self.make_api_header()

        dev_list_url = f'{self.host_domain}/v1.0/devices'
        response = (
            requests.get(
                url=dev_list_url,
                headers=api_header
            )
        )
        # ステータスコードが4xx/5xxの場合は例外を発生させる
        response.raise_for_status()
        
        device_list = response.json()['body']['deviceList']
        for device in device_list:
            # スマートロックが1台の場合のみ通用
            if device['deviceType'] == 'Smart Lock':
                self.device_id = device['deviceId']
                break
    
    def switch_lock_status(self):
        status = self.get_lock_status()

        # 開いている場合は施錠する
        if status == 'locked':
            self.send_ctrl_cmd('unlock')
        # 閉まっている場合は解錠する
        elif status == 'unlocked':
            self.send_ctrl_cmd('lock')

    def get_lock_status(self):
        api_header = self.make_api_header()
        dev_status_url = f'{self.host_domain}/devices/v1.1/{self.device_id}/status'

        response = (
            requests.get(
                url=dev_status_url,
                headers=api_header
            )
        )
        response.raise_for_status()
        
        status = response.json()['body']['lockState']
        return status

    def send_ctrl_cmd(self, cmd: str):
        api_header = self.make_api_header()
        dev_ctrl_url = f'{self.host_domain}/devices/v1.1/{self.device_id}/commands'
        
        response = (
            requests.post(
                url=dev_ctrl_url,
                headers=api_header,
                json={
                    'commandType': 'command',
                    'command': cmd,
                    'parameter': 'default'
                }
            )
        )
