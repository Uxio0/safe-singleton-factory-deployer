import os

import requests
from eth_account import Account
from hexbytes import HexBytes
from web3 import Web3
from werkzeug.exceptions import HTTPException

MNEMONIC = os.environ["MNEMONIC"]
Account.enable_unaudited_hdwallet_features()
DEPLOYER_ACCOUNT = Account.from_mnemonic(MNEMONIC)
CONTRACT_DEPLOYMENT_CODE = HexBytes(
    "0x604580600e600039806000f350fe7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe03601600081602082378035828234f58015156039578182fd5b8082525050506014600cf3"
)
MINIMUM_DEPLOY_GAS = os.environ.get("MINIMUM_DEPLOY_GAS", 100_000)


class ChainNotSupported(HTTPException):
    code = 422
    description = "Chain not supported, please send a PR to https://github.com/ethereum-lists/chains"


class NotEnoughFunds(HTTPException):
    code = 422


class ContractIsAlreadyDeployed(HTTPException):
    code = 422
    description = "Contract is already deployed"


def check_chain_id(chain_id: int) -> bool:
    url = (
        f"https://chainlist.org/_next/data/cTmGuUPQ4QLoYHDQ-Zzz6/chain/{chain_id}.json"
    )
    response = requests.get(url)
    return response.ok


def deploy_contract(rpc_url: str) -> HexBytes:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    chain_id = w3.eth.chain_id
    if not check_chain_id(chain_id):
        raise ValueError()

    tx = {
        "from": DEPLOYER_ACCOUNT.address,
        "data": CONTRACT_DEPLOYMENT_CODE,
    }
    gas_estimated = w3.eth.estimate_gas(tx)

    tx["nonce"] = 0
    tx["gas"] = max(MINIMUM_DEPLOY_GAS, gas_estimated)
    tx["gasPrice"] = w3.eth.gas_price
    tx["chainId"] = chain_id

    signed = DEPLOYER_ACCOUNT.sign_transaction(tx)
    try:
        return w3.eth.send_raw_transaction(signed.rawTransaction)
    except ValueError as exc:
        if "nonce" in str(exc).lower():
            raise ContractIsAlreadyDeployed()
        else:
            # No funds
            required_funds = tx["gasPrice"] * tx["gas"]
            required_funds_eth = Web3.fromWei(required_funds, "ether")
            raise NotEnoughFunds(
                f"Required at least {required_funds} wei ({required_funds_eth} eth). Send funds to {DEPLOYER_ACCOUNT.address}"
            )
