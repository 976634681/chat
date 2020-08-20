"""
chat room 客户端
发送请求 接收消息
"""
from socket import *
from multiprocessing import Process
import sys

# 服务器地址
ADDR = ("127.0.0.1", 8000)


# 进入聊天室
def login(sock):
    while True:
        name = input("请输入聊天室昵称:")
        # 给服务端发送请求
        msg = "LOGIN " + name  # 根据协议组织消息
        sock.sendto(msg.encode(), ADDR)
        # 等待结果
        result, addr = sock.recvfrom(128)
        # 约定ok作为请求成功的标志
        if result.decode() == "ok":
            print("进入聊天室")
            return name  # 以name登录
        else:
            print("名称已被占用，请重新输入！")


def recv_msg(sock):
    while True:
        data, addr = sock.recvfrom(1024 * 10)
        # 美化打印内容
        msg = "\n" + data.decode() + "\n发送:"
        print(msg, end="")


def send_msg(sock, name):
    while True:
        try:
            content = input("发送:")
        except KeyboardInterrupt:
            content = "exit"
            # 输入exit要退出
        if content == "exit":
            msg = "EXIT " + name
            sock.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = "CHAT %s %s" % (name, content)
        sock.sendto(msg.encode(), ADDR)


def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    # sock.sendto("测试信息".encode(),ADDR)

    # 进入聊天室
    name = login(sock)

    # 创建子进程
    p = Process(target=recv_msg, args=(sock,))
    p.daemon = True  # 子进程随着父进程退出
    p.start()
    send_msg(sock, name)  # 父进程发送消息


if __name__ == '__main__':
    main()

