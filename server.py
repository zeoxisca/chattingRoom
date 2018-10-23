from socket import *
import json
import hashlib
import time
import threading

users = {}
commands = [
    'chat',
    'login',
    'reg',
    'priv',
    'exit',
    'logout'
]

#{'

#{'cmd':'chat',


def deal(text, _addr):
    _status = {}
    json_text = json.loads(text)
    command = json_text['cmd']

    if command not in commands:  # 没有命令
        _status['code'] = 100
        _status['msg'] = 'command wrong'
        return json.dumps(_status)

    if command == 'chat':
        pass

    elif command == 'login':
        try:
            _ip = _addr[0]
            name = json_text['data']['name']
            password = json_text['data']['password']
        except Exception as e:
            _status['code'] = 500
            _status['msg'] = 'data wrong'
            return json.dumps(_status)

        error_code = login(name, password, _ip)
        if error_code == 0:
            _status['code'] = 300
            _status['msg'] = 'no register'

        elif error_code == 1:
            _status['code'] = 301
            _status['msg'] = "couldn't login"

        elif error_code == 2:
            _status['code'] = 302
            _status['msg'] = "login_ed"

        elif error_code == 4:
            _status['code'] = 304
            _status['msg'] = "user error, please reregister"

        elif error_code == 3:
            _status['code'] = 200
            _status['msg'] = "login success"

        else:
            _status['code'] = 500
            _status['msg'] = "unknown error"

        return json.dumps(_status)

    elif command == 'reg':
        try:
            _ip = _addr[0]
            name = json_text['data']['name']
            password = json_text['data']['password']
        except Exception as e:
            _status['code'] = 500
            _status['msg'] = 'data wrong'
            return json.dumps(_status)

        error_code = register(name, password, _ip)

        if error_code == 2:
            _status['code'] = 302
            _status['msg'] = 'login_ed'

        elif error_code == 1:
            _status['code'] = 200
            _status['msg'] = 'register success'

        elif error_code == 0:
            _status['code'] = 600
            _status['msg'] = 'registered'

        else:
            _status['code'] = 500
            _status['msg'] = 'unknown error'

        return json.dumps(_status)

    elif command == 'priv':
        try:
            _ip = _addr[0]
            msg = json_text['data']['msg']
            aim_name = json_text['data']['aim']
            aim_ip = users[aim_name]['ip']
            from_name = json_text['data']['name']

        except Exception as e:
            _status['code'] = 500
            _status['msg'] = 'data wrong'
            return json.dumps(_status)

        stat = chat_2(from_name, msg, aim_ip)
        if stat:
            _status['code'] = 200
            _status['msg'] = 'success'
            return json.dumps(_status)
        else:
            _status['code'] = 505
            _status['msg'] = "can't send"
            return json.dumps(_status)
    # elif command == 'logout':



def refile():
    with open('./pass.txt', 'w') as file:
        for key in users:
            temp = []
            temp.append(key)
            temp.append(str(users[key]['passhash']))
            temp.append(str(users[key]['login_time']))
            temp.append(str(users[key]['register_time']))
            temp.append(str(users[key]['ip']))
            file.write(';'.join(temp))


def login(name, password, _ip):
    try:
        _status = users[name]
    except Exception as e:
        return 0  # 未注册
    if _status['status'] == 1:
        return 2  # 已登录

    if _status['register_time'] == '':
        del users[name]
        refile()
        return 4  # 账号异常

    pass_hash = _status['passhash']

    m2 = hashlib.md5()
    m2.update(password.encode('utf-8'))
    h = m2.hexdigest()

    if h == pass_hash:
        users[name]['login_time'] = int(time.time())
        users[name]['status'] = 1
        users[name]['ip'] = _ip
        return 3  # 登陆成功

    return 1  # 登录失败


def register(name, password, _ip):

    for values in users.values():
        if values['status'] == 1 and values['ip'] == _ip:
            return 2  # 已登录

    try:
        user = users[name]
        return 0  # 已注册
    except Exception as e:
        users[name] = {}
        users[name]['login_time'] = 0
        users[name]['register_time'] = int(time.time())
        users[name]['status'] = 0  # 未登录

        m2 = hashlib.md5()
        m2.update(password.encode('utf-8'))
        h = m2.hexdigest()

        users[name]['passhash'] = h

        users[name]['ip'] = _ip

        refile()
        return 1  # 注册成功


def chat_2(from_name, msg, aim_ip):
    _addr = (aim_ip, 57070)
    bufSize = 1024
    _status = {}
    _status['code'] = 1000
    _status['msg'] = {
        'from': from_name,
        'text': msg
    }
    data = json.dumps(_status)
    try:
        udpServer.sendto(data.encode('utf-8'), _addr)
        return 1
    except Exception:
        return 0


if __name__ == '__main__':
    with open('./pass.txt', 'r') as file:
        user = file.readlines()
        for i in user:
            temp = i.split(';')
            if len(temp) >= 2:
                users[temp[0]] = {}
                users[temp[0]]['login_time'] = temp[2]
                users[temp[0]]['register_time'] = temp[3]
                users[temp[0]]['status'] = 0  # 未登录
                users[temp[0]]['passhash'] = temp[1]
                try:
                    users[temp[0]]['ip'] = temp[4]
                except Exception as e:
                    users[temp[0]]['ip'] = ''
            else:
                exit('something wrong')

    host = ''
    port = 12315
    bufSize = 1024
    addr = (host, port)

    udpServer = socket(AF_INET, SOCK_DGRAM)
    udpServer.bind(addr)

    while True:
        data, new_addr = udpServer.recvfrom(bufSize)
        raw_input = data.decode('utf-8')
        if raw_input == 'quit':
            break

        status = deal(raw_input, new_addr)
        data = status.encode('utf-8')


        udpServer.sendto(data, new_addr)

    udpServer.close()