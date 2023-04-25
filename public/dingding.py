import time
import urllib.parse
import base64
import hmac
import hashlib
import requests



#配置发送钉钉
def sed_dingding(text):
    if text:
        timestamp = str(round(time.time() * 1000))
        ser='SEC6d383bbb2abf60d6db0a049d9bb7e4bee4565b71040dbc7b7ccfbfbbe823717f'
        secret = ser
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # print(timestamp)
        # print(sign)
        url="https://oapi.dingtalk.com/robot/send?access_token=2931d30ac239c39fd435c533990108e471ff3b591122060fb58227bfed789ac2&sign="
        url_count=url+sign+'&timestamp='+timestamp
        # print(url_count)

        headers={
        "Content-Type": "application/json; charset=utf-8"
        }

        params={"msgtype": "text","text": {"content":text}}

        re=requests.post(url_count,headers=headers,json=params)
        # print(re)
        return re
    else:
        return {'data':'钉钉发送数据不能为空！'}