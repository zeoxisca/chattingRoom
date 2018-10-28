from socket import *
import json
import time
import threading

host = '127.0.0.1'
port = 12315
bufSize = 1024
addr = (host, port)
exit_sign = False
udpClient = socket(AF_INET, SOCK_DGRAM)
udpClient.bind(('127.0.0.1', 57070))


_name = ''
temp_name = ''
commands = [
    'login',
    'reg',
    'priv',
    'exit',
    'logout'
]

rcv = []


def deal(msg):
    global temp_name
    message = {}
    command = 'chat'
    if msg[0] != '/':
        if _name == '':
            return 0
        message['cmd'] = command
        message['data'] = {
            'text': msg,
            'name': _name
        }
        return json.dumps(message)
    else:
        temp = msg.split(' ')
        if len(temp) <= 1:
            return 1
        if temp[0][1:] not in commands:
            return 2

        if temp[0][1:] == 'login':
            try:
                name = temp[1]
                password = temp[2]
            except Exception as e:
                return 3
            message['cmd'] = 'login'
            message['data'] = {
                'name': name,
                'password': password
            }
            temp_name = name

            return json.dumps(message)
        if temp[0][1:] == 'reg':
            try:
                name = temp[1]
                password = temp[2]
                cr_password = temp[3]
            except Exception as e:
                return 3
            if cr_password != password:
                return 4
            message['cmd'] = 'reg'

            message['data'] = {
                'name': name,
                'password': password
            }
            return json.dumps(message)

        if temp[0][1:] == 'priv':
            if _name == '':
                return 0
            try:
                aim_name = temp[1]
                text = temp[2]
                from_name = _name
            except Exception as e:
                return 3
            message['cmd'] = 'priv'
            message['data'] = {
                'aim': aim_name,
                'msg': text,
                'name': from_name
            }

            return json.dumps(message)

        if temp[0][1:] == 'exit':
            return 'exit'

    return 3


def deal_rcv(rcv):
    global _name

    rcv = json.loads(rcv)
    _code = rcv['code']
    if _code == 100:
        print('无此命令')
        return 1
    if _code == 500:
        print('数据错误')
        return 1
    if _code == 300:
        print('还没注册成功')
        return 1
    if _code == 301:
        print('登录失败')
        return 1
    if _code == 302:
        pass

    if _code == 1000:
        name = rcv['msg']['from']
        msg = rcv['msg']['text']
        print(name, ' ', time.strftime("%H:%M:%S"))
        print(msg)
        return 'OK'

    if _code == 200:
        if rcv['msg'] == 'login success':
            print('登陆成功')
            _name = temp_name

        return 'OK'
    else:
        print('不成功')
        return 1


def inin():
    global udpClient
    while True:
        msg = input('a')
        if len(msg) == 0:
            continue
        text = deal(msg)
        if text == 0:
            print('先登录')
            continue
        if text == 1:
            print('命令错误')
            continue
        if text == 2:
            print('无此命令')
            continue
        if text == 3:
            print('格式错误')
            continue
        if text == 4:
            print('密码错误')
            continue
        if text == 'exit':
            break
        try:
            udpClient.sendto(text.encode('utf-8'), addr)
        except BaseException as e:
            print('请重新发送')
            continue


def user_recv():
    global udpClient
    while True:
        try:
            recv, new_addr = udpClient.recvfrom(bufSize)
            rcv.append(recv.decode('utf-8'))
        except:
            pass
        # if status != 'OK':
        #     continue


def user_deal():
    while True:
        try:
            status = deal_rcv(rcv.pop(0))
        except Exception as e:
            continue


if __name__ == '__main__':

    user_in = threading.Thread(target=inin, args=())
    user_d = threading.Thread(target=user_deal, args=())
    user_r = threading.Thread(target=user_recv, args=())

    user_in.start()
    user_d.start()
    user_r.start()

    udpClient.close()