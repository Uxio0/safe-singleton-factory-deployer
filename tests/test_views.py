from flaskr.services import DEPLOYER_ACCOUNT

from .utils import send_ether


def test_main_view(client):
    response = client.post("/")
    assert response.status_code == 400

    invalid_rpc = "http://localhost:8546"
    response = client.post("/", json={"rpc": invalid_rpc})
    assert response.json == {
        "code": 422,
        "name": "Unprocessable Entity",
        "description": f"Error connecting to RPC {invalid_rpc}",
    }

    valid_rpc = "http://localhost:8545"
    response = client.post("/", json={"rpc": valid_rpc})
    assert response.status_code == 422
    assert "Required at least" in response.json["description"]
    assert f"Send funds to {DEPLOYER_ACCOUNT.address}" in response.json["description"]

    send_ether(valid_rpc, 1, DEPLOYER_ACCOUNT.address)
    response = client.post("/", json={"rpc": valid_rpc})
    assert response.status_code == 200
    assert response.json["txHash"][:2] == "0x"
    assert len(response.json["txHash"]) == 66

    send_ether(valid_rpc, 1, DEPLOYER_ACCOUNT.address)
    response = client.post("/", json={"rpc": valid_rpc})
    assert response.status_code == 422
    assert response.json == {
        "code": 422,
        "description": "Contract is already deployed",
        "name": "Unprocessable Entity",
    }
