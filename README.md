# safe-singleton-factory-deployer

Automatic deployer for https://github.com/safe-global/safe-singleton-factory

## Configuration for deployment
- Set `MNEMONIC` environment variable with a valid words mnemonic
- `gunicorn -w 4 -b 0.0.0.0:8888 'flaskr:create_app()'`

## Usage

- On the url that's running send a `POST` request with the following JSON:
```json
{
  "rpc": "http://your-network-rpc"
}
```

```json
{
    "code": 422,
    "name": "Unprocessable Entity",
    "description": "Required at least 4999273600400000 wei (0.0049992736004 eth). Send funds to 0xE1CB04A0fA36DdD16a06ea828007E35e1a3cBC37"
}
```
You need to send funds to the deployer and then if everything goes well this response will be returned:
```json
{
  "txHash": "<0x prefixed transaction hash>"
}
```
