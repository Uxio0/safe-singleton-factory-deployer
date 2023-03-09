from eth_account import Account

from flaskr.services import check_chain_id

GANACHE_FIRST_ACCOUNT = Account.from_key(
    "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"
)


def test_check_chain_id():
    assert check_chain_id(100)
    assert not check_chain_id(151515151515151)
