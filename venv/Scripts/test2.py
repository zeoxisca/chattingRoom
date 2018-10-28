import threading
import socket

z = ''
z1 = ''


def inin():
    while True:
        try:
            m, new_addr = udpClient.recvfrom(bufSize)
            a.append(m.decode('utf-8'))
        except ConnectionError as e:
            print(e)
            continue
        except:
            print("unexpected")
            continue


def ouou():
    a = [1, 2, 3, 4, 5]
    while True:
        try:
            udpClient.sendto(str(a.pop()).encode('utf-8'), addr)
        except ConnectionError as e:
            print(e)
            continue
        except:
            print("unexpected")
            continue


if __name__ == "__main__":
    udpClient = socket.socket(AF_INET, SOCK_DGRAM)
    udpClient.bind(('', 12315))
    host = '127.0.0.1'
    port = 12315
    bufSize = 1024
    addr = (host, port)
    while True:
        m, new_addr = udpClient.recvfrom(bufSize)
        udpClient.sendto(m, new_addr)


