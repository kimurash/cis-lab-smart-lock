import base64
import hashlib
import hmac
import os
import time
import uuid

from dotenv import load_dotenv
import requests


host_domain = 'https://api.switch-bot.com'


def make_api_header(credentials: dict):
    # Declare empty header dictionary
    api_header = {}

    nonce = uuid.uuid4()
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(credentials['token'], t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(credentials['secret'], 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    # Build api header JSON
    api_header['Authorization'] = credentials['token']
    api_header['Content-Type'] = 'application/json'
    api_header['charset'] = 'utf8'
    api_header['t'] = str(t)
    api_header['sign'] = str(sign, 'utf-8')
    api_header['nonce'] = str(nonce)

    return api_header

def get_device_id(credentials: dict):
    api_header = make_api_header(credentials)

    dev_list_url = f'{host_domain}/v1.1/devices'
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
            return device['deviceId']

def switch_lock_status(credentials: dict, device_id: str):
    status = get_lock_status(credentials, device_id)

    # 開いている場合は施錠する
    if status == 'locked':
        send_ctrl_cmd(credentials, 'unlock')
    # 閉まっている場合は解錠する
    elif status == 'unlocked':
        send_ctrl_cmd(credentials, 'lock')

def get_lock_status(credentials: dict, device_id: str):
    api_header = make_api_header(credentials)
    dev_status_url = f'{host_domain}/v1.1/devices/{device_id}/status'

    response = (
        requests.get(
            url=dev_status_url,
            headers=api_header
        )
    )
    response.raise_for_status()
    
    status = response.json()['body']['lockState']
    return status

def send_ctrl_cmd(credentials: dict, cmd: str):
    api_header = make_api_header(credentials)
    dev_ctrl_url = f'{host_domain}/v1.1/devices/{device_id}/commands'
    
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

if __name__ == '__main__':
    load_dotenv()

    TOKEN  = os.getenv('SWITCHBOT_TOKEN')
    SECRET = os.getenv('SWITCHBOT_SECRET')
    credentials = {
        'token': TOKEN,
        'secret': SECRET
    }
    
    device_id = get_device_id(credentials)
    switch_lock_status(credentials, device_id)
