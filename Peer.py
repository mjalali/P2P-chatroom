from Message import Message


Max_message_size = 1024


class Peer:
    def __init__(self, sock_client, ip, port_num, my_private_key, my_public_key, public_key, P, name="unknown"):
        self.sock_client = sock_client
        self.ip = ip
        self.port_num = port_num
        self.my_public_key = my_public_key
        self.messages = Message(my_private_key, public_key, P)
        self.name = name
        self.set_name(name)
        self.is_online = False

    def set_is_online(self, x):
        self.is_online = x

    def set_name(self, name):
        if name != "unknown":
            self.name = name
        else:
            # should search in contacts
            pass

    def recv_message(self):
        while True:
            text = self.sock_client.recv(Max_message_size)
            text = str(text)
            text = text[2:-1]
            plain_text = self.messages.crypto_obj.decrypt(text)
            self.messages.add_message(self.name + "->" + plain_text + "(" + text + ")")
            if self.is_online is True:
                ob = self.messages.objects[-1]
                print(f"{ob['text']}, {ob['time']}")

    def send_message(self):
        print("type return to return to inbox")
        print("me->", end="")
        while True:
            plain_text = str(input())
            if plain_text == "return":
                break
            if len(plain_text) > Max_message_size:
                print("too big message!")
            text = self.messages.crypto_obj.encrypt(plain_text)
            self.messages.add_message(self.name + "->" + plain_text + "(" + text + ")")
            self.sock_client.send(text.encode("utf8"))
