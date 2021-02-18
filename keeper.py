from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes
from hashlib import sha256
from sys import argv
from contract import KeeperAPI
import secrets
import logging


class Keeper():

    ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&?@_'

    USERNAME_LENGTH = 12

    LABEL_LENGTH = 32

    def __init__(self, master_key, contract_address, infura_provider, private_key):
        self.master_key = sha256(bytes(master_key, 'utf-8')).digest()
        self.contract = KeeperAPI('smart contracts/Keeper.sol', contract_address, infura_provider, private_key)

    def oracle(self, msg, nonce=None):
        aes = AES.new(self.master_key, AES.MODE_CTR, nonce=nonce)
        nonce = aes.nonce

        return aes.encrypt(msg), nonce

    def generatePassword(self, username=None):
        password = ''.join([secrets.choice(self.ALPHABET) for _ in range(12)])

        target = password + username

        encrypted_target, nonce = self.oracle(target.encode('utf-8'))

        return bytes_to_long(encrypted_target + nonce)

    def uploadPassword(self, target, label):
        logging.info(f'target: {target}\n label: {label}\n')

    def getPassword(self, label):
        target = long_to_bytes(int(input('target: ')))

        print(self.oracle(target[:-8], target[-8:]))

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
                        label = input(f'[~] Label(Must be between 1 and {self.LABEL_LENGTH} characters long): ')
                        assert len(label) in range(1, self.LABEL_LENGTH + 1)
                        break
                    except AssertionError:
                        logging.error(f'[-] Label Must be between 1 and {self.LABEL_LENGTH} characters long')

                while True:
                    try:
                        username = input(f'[~] Username({self.USERNAME_LENGTH} characters max, hit enter to leave empty): ')
                        assert len(username) <= self.USERNAME_LENGTH
                        break
                    except AssertionError:
                        logging.error(f'[-] Username Must be {self.USERNAME_LENGTH} characters max')

                target = self.generatePassword(username)
                self.uploadPassword(target, label)

            elif choice == 4:
                while True:
                    try:
                        label = input(f'[~] Label(Must be between 1 and {self.LABEL_LENGTH} characters long): ')
                        assert len(label) in range(1, self.LABEL_LENGTH + 1)
                        break
                    except AssertionError:
                        logging.error(f'[-] Label Must be between 1 and {self.LABEL_LENGTH} characters long')

                self.getPassword(label)
            else:
                break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    if len(argv) < 5:
        logging.error('[-] Usage: python keeper.py <master key> <contract address> <infura provider> <private key>')
        exit(0)

    keeper = Keeper(*argv[1:])
    keeper.main()
