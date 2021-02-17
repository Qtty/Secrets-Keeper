from Crypto.Cipher import AES
from hashlib import sha256
from os import urandom
from sys import argv
from base64 import b64encode, b64decode
from json import dumps, loads
import secrets
import logging


class Keeper():

    ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&?@_'

    def __init__(self, master_key):
        self.master_key = sha256(bytes(master_key, 'utf-8')).digest()

    def oracle(self, msg, nonce=None):
        aes = AES.new(self.master_key, AES.MODE_CTR, nonce=nonce)
        nonce = aes.nonce

        return aes.encrypt(msg), nonce

    def generatePassword(self, username=None):
        password = ''.join([secrets.choice(self.ALPHABET) for _ in range(20)])

        target = {'password': password, 'username': username}
        target = dumps(target).encode('utf-8')

        encrypted_target, nonce = self.oracle(target)

        return b64encode(encrypted_target), nonce

    def uploadPassword(self, target:bytes, label:str, nonce: bytes):
        logging.info(f'target: {target}\n label: {label}\n nonce: {nonce.hex()}')

    def getPassword(self, label):
        nonce = bytes.fromhex(input('nonce: '))
        target = b64decode(input('target: ').encode('utf-8'))

        print(self.oracle(target, nonce))

    def main(self):
        while True:
            print('[~] which operation would you like to perform?\n')
            print('[1] Generate a new Password')
            print('[2] Update an already existing Password')
            print('[3] Remove a Password')
            print('[4] Retreive a Password')
            print('[5] Exit\n')

            try:
                choice = int(input('[~] choice: '))
                assert choice in range(1, 6)
            except (AssertionError, TypeError):
                logging.error('[-] Choice must be 1, 2, 3, 4 or 5\n')
                continue

            if choice == 1:
                while True:
                    try:
                        label = input('[~] Label(Must be between 1 and 20 characters long): ')
                        assert len(label) in range(1, 21)
                        break
                    except AssertionError:
                        logging.error('[-] Label Must be between 1 and 20 characters long')
                
                while True:
                    try:
                        username = input('[~] Username(20 characters max, hit enter to leave empty): ')
                        assert len(username) <= 20
                        break
                    except AssertionError:
                        logging.error('[-] Username Must be 20 characters max')

                target, nonce = self.generatePassword(username)
                self.uploadPassword(target, label, nonce)

            elif choice == 4:
                while True:
                    try:
                        label = input('[~] Label(Must be between 1 and 20 characters long): ')
                        assert len(label) in range(1, 21)
                        break
                    except AssertionError:
                        logging.error('[-] Label Must be between 1 and 20 characters long')

                self.getPassword(label)
            else:
                break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if len(argv) < 1:
        logging.error('[-] Usage: python keeper.py <master key>')
        exit(0)

    keeper = Keeper(argv[1])
    keeper.main()