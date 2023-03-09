import os
from functools import cache

import requests
from eth_account import Account
from eth_account.signers.local import LocalAccount
from hexbytes import HexBytes
from web3 import Web3

from .exceptions import (
    ChainNotSupported,
    ContractIsAlreadyDeployed,
    NotEnoughFunds,
    RPCConnectionError,
)

CONTRACT_DEPLOYMENT_CODE = HexBytes(
    "0x604580600e600039806000f350fe7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe03601600081602082378035828234f58015156039578182fd5b8082525050506014600cf3"
)


@cache
def get_deployer_account() -> LocalAccount:
    Account.enable_unaudited_hdwallet_features()
    mnemonic = os.environ.get("MNEMONIC")
    return Account.from_mnemonic(mnemonic) if mnemonic else Account.create()


@cache
def get_minimum_deploy_gas():
    return os.environ.get("MINIMUM_DEPLOY_GAS", 100_000)


def check_chain_id(chain_id: int) -> bool:
    url = (
        f"https://chainlist.org/_next/data/cTmGuUPQ4QLoYHDQ-Zzz6/chain/{chain_id}.json"
    )
    response = requests.get(url)
    return response.ok


def deploy_contract(rpc_url: str) -> HexBytes:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    deployer_account = get_deployer_account()

    try:
        account_nonce = w3.eth.get_transaction_count(deployer_account.address)
        if account_nonce != 0:
            raise ContractIsAlreadyDeployed
    except IOError:
        raise RPCConnectionError(f"Error connecting to RPC {rpc_url}")

    chain_id = w3.eth.chain_id
    if not check_chain_id(chain_id):
        raise ChainNotSupported(
            f"Chain {chain_id} not supported, please send a PR to https://github.com/ethereum-lists/chains"
        )

    tx = {
        "from": deployer_account.address,
        "data": CONTRACT_DEPLOYMENT_CODE,
    }
    gas_estimated = w3.eth.estimate_gas(tx)

    tx["nonce"] = 0
    tx["gas"] = max(get_minimum_deploy_gas(), gas_estimated)
    tx["gasPrice"] = w3.eth.gas_price
    tx["chainId"] = chain_id

    signed = deployer_account.sign_transaction(tx)
    try:
        return w3.eth.send_raw_transaction(signed.rawTransaction)
    except ValueError as exc:
        # No funds
        required_funds = tx["gasPrice"] * tx["gas"]
        required_funds_eth = Web3.fromWei(required_funds, "ether")
        raise NotEnoughFunds(
            f"Required at least {required_funds} wei ({required_funds_eth} eth). Send funds to {deployer_account.address}"
        )
