from threading import Thread
from Peer import *
import socket
import sys
from threading import Thread
import traceback
import random

peers = []
P = 0x0264fa447670ea82537279828fb9a515ab
G = 0x2
my_pr = random.choice(range(P - pow(2, 30), P))
my_pu = pow(G, my_pr, P)


def establish_connection(ip_addr, port_num):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((ip_addr, int(port_num)))
    sock.send(str(my_pu).encode("utf8"))
    public_key = int(sock.recv(Max_message_size).decode("utf8"))
    new_peer = Peer(sock, ip_addr, port_num, my_pr, my_pu, public_key, P)
    return new_peer


def answer():
    while True:
        print("hi! your inbox:")
        if len(peers) == 0:
            print("your inbox is empty!")
            print("press 1 to refresh or 0 to exit")
            x = int(input())
            if x == 0:
                return
        else:
            x = 0
            for peer in peers:
                print(str(x) + "-> " + peer.name + str((peer.ip, peer.port_num)))
                x += 1
            y = int(input())
            peers[y].messages.show_history()
            peers[y].set_is_online(True)
            peers[y].send_message()


def start_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    sock.listen()
    while True:
        connection, address = sock.accept()
        connection.send(str(my_pu).encode("utf8"))
        public_key = int(connection.recv(Max_message_size).decode("utf8"))
        new_peer = Peer(connection, address[0], address[1], my_pr, my_pu, public_key, P)
        peers.append(new_peer)
        try:
            Thread(target=new_peer.recv_message, args=()).start()
        # except timeout:
        #    break
        except:
           traceback.print_exc()


def Exit_peer():
    for peer in peers:
        peer.sock_client.close()


def main():
    host = "127.0.0.1"
    port = 1234
    server_thread = Thread(target=start_server, args=(host, port))
    server_thread.start()
    while True:
        print("please enter what you what to do:")
        print("0.new message   1.check inbox   2.exit")
        x = int(input())
        if x == 0:
            print("enter ip and port number:")
            ip_addr = str(input())
            port_num = int(input())
            new_peer = establish_connection(ip_addr, port_num)
            peers.append(new_peer)
            try:
                Thread(target=new_peer.recv_message, args=()).start()
            # except timeout:
            #    break
            except:
                traceback.print_exc()
            new_peer.set_is_online(True)
            new_peer.send_message()
        if x == 1:
            answer()
        if x == 2:
            Exit_peer()
            break


if __name__ == "__main__":
    main()
