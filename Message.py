from datetime import datetime
from Cryptography import Cryptography


class Message:
    def __init__(self, private_key, public_key, P):
        self.crypto_obj = Cryptography(private_key, public_key, P)
        self.objects = []

    def add_message(self, text, time=datetime.now(), seen=False):
        self.objects.append({'text': text, 'time': time, 'seen': seen})

    def show_history(self):
        for ob in self.objects:
            print(f"{ob['text']}, {ob['time']}")
