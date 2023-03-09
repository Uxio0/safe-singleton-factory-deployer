from eth_account import Account
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import Web3

GANACHE_FIRST_ACCOUNT = Account.from_key(
    "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
)


def send_ether(rpc_url: str, eth: int, to: ChecksumAddress) -> HexBytes:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    signed = GANACHE_FIRST_ACCOUNT.sign_transaction(
        {
            "to": to,
            "value": Web3.toWei(eth, "ether"),
            "chainId": w3.eth.chain_id,
            "gas": 23_000,
            "gasPrice": w3.eth.gas_price,
            "nonce": w3.eth.get_transaction_count(GANACHE_FIRST_ACCOUNT.address),
        }
    )
    return w3.eth.send_raw_transaction(signed.rawTransaction)
