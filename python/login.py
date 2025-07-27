import time

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import streamlit as st

def encrypt(password):
    key = '20171109124536982017110912453698'.encode('utf-8')
    iv = '2017110912453698'.encode('utf-8')
    chiper = AES.new(key, AES.MODE_CBC, iv)
    encrypted = chiper.encrypt(pad(password.encode('utf-8'), AES.block_size))
    return encrypted.hex().upper()

def get_token(username, password, url) -> tuple[int, str]:
    if username == '' or password == '':
        return 4, ''
    try:
        resp = requests.post(url, json={
            "platform": 1,
            "userName": username,
            "password": encrypt(password),
            "autoLogin": True,
            "webVersion": "0"
        },headers={
            'timestamp': str(int(time.time())),
            'platform': '1',
            'sign': '0',
            'secretId': '0',
            'token': '0'
        })
        resp.raise_for_status()
        resp_json = resp.json()
        if resp_json.get('data'):
            return 0, resp_json.get('data').get('token')
        elif resp_json.get('msg') == '账号或密码错误':
            return 1, ''
        elif resp_json.get('msg') == '请完成安全验证后再登录':
            return 2, ''
        elif resp_json.get('msg') == '登录密码错误超限，请进行安全校验':
            return 3, ''
        elif resp_json.get('msg') == '参数不合法:账号/手机号不能为空':
            return 4, ''
        else:
            return -1, resp_json.get('msg')
    except requests.exceptions.RequestException as e:
        st.error(f"请求失败: {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        st.error("请检查各项内容是否正确填写。")
        st.stop()


