# Secrets Keeper

A Password Generation and Storing tool built with with Python and Solidity.

## Overview

The idea is to `generate passwords using Python`, encrypt them along with a `label`(for ex: github) and optionally a `username`, This info is then `encrypted` using a `master key` and `stored` in the `ethereum blockchain` using a `smart contract`.

To `retrieve` a certain password, simply `query` the smart contract using the `label`, and there's the possibility to `retrieve all labels` from the smart contract.

Note that the master key is `required` to retreive labels and/or passwords, since everything is `encrypted` in the smart contract to avoid exposing which services a client is using

## Setup

### Python

To setup the Python part, simply start a new virtualenv, and install the dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
PS: the python version used during developement is `3.8.5`

### Sodility

For this part, check the [official guide](https://docs.soliditylang.org/en/v0.8.0/installing-solidity.html) on how to install the compiler

## Getting Started

So in order to start, you'll need three things:

1. A Ethereum Wallet
2. Funds in that Wallet
3. An Infura Provider

Don't worry, it's totally free :)

### Creating an Ethereum Wallet

The easiest way to create an ethereum wallet is to install `MetaMask` browser extension and create an account, it'll give you an ethereum wallet and a the private key to that wallet, copy that key so that you can user it later.

### Getting Funds

So now, there are many networks in ethereum blockchain:
* there's the main network, in which transactions are dealt using real money purchased ether
* there are testing networks, which have facets that provide you with free ether for testing, 1 ether, which will largely suffice.

Now if you want to use the mainnet, you'll need to purchase ether to perform transactions, note that you'll be spending ether in these three situations:

* When Creating the Smart Contract
* When Generating Passwords
* When Removing Passwords

But it's best to use the testing networks like the `Ropsten` network, i'll update this with the info regarding the `lifetime` of the `Testing networks`.

### Infura Provider

#### Overview

to keep it short, here's some quotes that explain what's a provider, and what's Infura:

[Web3.py Docs](https://web3py.readthedocs.io/en/stable/providers.html):

> The provider is how web3 talks to the blockchain.

[Truffle Suite](https://www.trufflesuite.com/tutorials/using-infura-custom-provider):

> Infura’s API suite provides instant HTTPS and WebSocket access to the Ethereum and IPFS networks. By using Infura, you can connect easily to Web 3.0 without having to spin-up and maintain your own infrastructure

visit the links above for more info.

#### Creating an Infura Provider

To get an Infura Provider:

1. Create an account in https://infura.io/
2. Login and go to the dashboard
3. Create a new project
4. After creating a project, go to the settings and get the provider' link, make sure to choose the endpoint where you deployed the Smart Contract

### Deploying the Smart Contract

in order to deploy the smart contract, run the following:
```bash
python deployer.py <infura provider> <private key>
```

and that's it! now a smart contract has beenn created, and only the transactions made from the address corresponding to that private key are allowed, so don't lose your private key ;)

### Generating and Storing Passwords

to start your the tool, simply run

```bash
python keeper.py <master key> <contract address> <infura provider> <private key>
```

* `master key`: the only key that you need to remember, it'll be used to encrypt the passwords, so keep it safe
* `contract address`: the address of the smart contract that you created
* `infura provider`: link to the infura provider
* `private key` your wallet's private key, it must be the same private key that was used to create the smart contract

A menu will pop up once you run the command above.