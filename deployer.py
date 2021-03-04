from web3 import Web3, HTTPProvider
from eth_account import Account
from solc import compile_standard
from json import loads
from sys import argv
import coloredlogs
import logging


class Deployer():
    ''' A script to deploy your contract '''

    def __init__(self, infura_provider, private_key):
        self.web3 = Web3(HTTPProvider(infura_provider, request_kwargs={'timeout': 60}))
        self.account = Account.from_key(private_key)
        self.web3.eth.default_account = self.account.address

    def getCompiledSol(self, path):
        with open(path, 'r') as f:
            source = f.read()

        fileName = path.split('/')[-1]
        contractName = fileName.replace('.sol', '')

        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {
                fileName: {
                    "content": source
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": [
                            "metadata", "evm.bytecode",
                            "evm.bytecode.sourceMap"
                        ]
                    }
                }
            }
        })

        bytecode = compiled_sol['contracts'][fileName][contractName]['evm']['bytecode']['object']
        abi = loads(compiled_sol['contracts'][fileName][contractName]['metadata'])['output']['abi']

        return bytecode, abi

    def deploy(self, path):
        bytecode, abi = self.getCompiledSol(path)
        Contract = self.web3.eth.contract(abi=abi, bytecode=bytecode)
        contract_txn = Contract.constructor().buildTransaction(
            {
                'from': self.account.address,
                'nonce': self.web3.eth.getTransactionCount(self.account.address),
                'gas': Contract.constructor().estimateGas(),
                'gasPrice': self.web3.eth.gas_price,
                'value': self.web3.toWei(0, 'ether')
            }
        )

        signed = self.account.signTransaction(contract_txn)
        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        logging.info(f'Transaction Hash: {tx_hash.hex()}')
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        if tx_receipt['status']:
            return tx_receipt.contractAddress

        raise RuntimeError('Transaction Failed')


if __name__ == '__main__':
    coloredlogs.install(level='info', fmt='%(msg)s')
    if len(argv) < 3:
        logging.error('Usage: python deployer.py <infura provider> <private key>')
        exit(0)

    deployer = Deployer(*argv[1:])
    logging.info(f"New Contract' Address: {deployer.deploy('smart contracts/Keeper.sol')}")
