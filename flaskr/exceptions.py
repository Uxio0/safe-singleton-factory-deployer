from werkzeug.exceptions import HTTPException


class ChainNotSupported(HTTPException):
    code = 422
    description = "Chain not supported, please send a PR to https://github.com/ethereum-lists/chains"


class NotEnoughFunds(HTTPException):
    code = 422


class ContractIsAlreadyDeployed(HTTPException):
    code = 422
    description = "Contract is already deployed"


class RPCConnectionError(HTTPException):
    code = 422
