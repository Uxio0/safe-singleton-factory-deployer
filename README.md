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

If everything goes well this response will be returned:
```json
{
  "txHash": "<0x prefixed transaction hash>"
}
```
