# Secrets Keeper

A Password Generation and Storing tool built with with Python and Solidity.

## Overview

The idea is to `generate passwords using Python`, encrypt them along with a `label`(for ex: github) and optionally a `username`, This info is then `encrypted` using a `master key` and `stored` in the `ethereum blockchain` using a `smart contract`.

To `retrieve` a certain password, simply `query` the smart contract using the `label`, and there's the possibility to `retrieve all labels` from the smart contract.

Note that the master key is `required` to retreive labels and/or passwords, since everything is `encrypted` in the smart contract to avoid exposing which services a client is using.