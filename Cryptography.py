from AES import AES


class Cryptography:
    def __init__(self, private_key, public_key, P):
        self.private_key = private_key
        self.public_key = public_key
        self.session_key = pow(public_key, private_key, P)
        self.aes_obj = AES(self.session_key)

    def encrypt(self, message):
        blocks = convertMessage(message)
        y = []
        for block in blocks:
            y.append(str(self.aes_obj.encrypt(block)))
        return '&'.join(y)

    def decrypt(self, message):
        x = []
        message = message.split("&")
        for block in message:
            x.append(self.aes_obj.decrypt(int(block)))
        return getMessage(x)


def convertMessage(string): # convert to blocks
    blocks = [string[i:i + (16 if (i + 16) <= len(string) else len(string) - i)] for i in range(0, len(string), 16)]
    for i in range(len(blocks)):
        blocks[i] = int('0x' + ''.join(hex(ord(c))[2:] for c in blocks[i]), 16)
    return blocks


def getMessage(blocks):  # decrypting and return original
    plaintext = ''
    for decrypted in blocks:
        decrypted = hex(decrypted)
        decrypted = [decrypted[i:i + 2] for i in range(2, len(decrypted), 2)]
        decrypted = [chr(int(c, 16)) for c in decrypted]
        plaintext += ''.join(decrypted)
    return plaintext

