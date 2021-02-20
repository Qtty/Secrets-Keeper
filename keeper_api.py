from deployer import Deployer


class KeeperAPI(Deployer):
    ''' A helper class that serves as an API for the smart contract '''

    def __init__(self, path, contract_address, infura_provider, private_key):
        super().__init__(infura_provider, private_key)
        bytecode, abi = self.getCompiledSol(path)
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)

    def getLabelsLength(self):
        return self.contract.functions.getLabelsLength().call()

    def getLabel(self, index):
        if index in range(self.getLabelsLength()):
            return self.contract.functions.labels(index).call()
        else:
            print('Operation will revert, index bigger than labels length')
            return -1

    def getTarget(self, label):
        return self.contract.functions.targets(label).call()

    def addPassword(self, label, target):
        previous_length = self.getLabelsLength()

        contract_txn = self.contract.functions.addPassword(label, target).buildTransaction(
            {
                'from': self.account.address,
                'nonce': self.web3.eth.getTransactionCount(self.account.address),
                'gas': self.contract.functions.addPassword(label, target).estimateGas(),
                'gasPrice': self.web3.eth.gas_price,
                'value': self.web3.toWei(0, 'ether')
            }
        )

        signed = self.account.signTransaction(contract_txn)
        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        print(f'Transaction Hash: {tx_hash.hex()}')
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        if tx_receipt['status'] and self.getLabelsLength() > previous_length:
            return True

        return False

    def removeLabel(self, index):
        previous_length = self.getLabelsLength()

        contract_txn = self.contract.functions.removeLabel(index).buildTransaction(
            {
                'from': self.account.address,
                'nonce': self.web3.eth.getTransactionCount(self.account.address),
                'gas': self.contract.functions.removeLabel(index).estimateGas(),
                'gasPrice': self.web3.eth.gas_price,
                'value': self.web3.toWei(0, 'ether')
            }
        )

        signed = self.account.signTransaction(contract_txn)
        tx_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction)
        print(f'Transaction Hash: {tx_hash.hex()}')
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        if tx_receipt['status'] and self.getLabelsLength() < previous_length:
            return True

        return False
