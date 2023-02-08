# Criteo api

criteo-api is a Python library for dealing with token authentication and requests for the Criteo
Retail Media Partner API

## Installation

TODO

```bash
TODO
```

## Usage

```python
from src import auth
from src import retail_media_api as rmapi
import json

# application credentials (downloaded .txt file from app portal in dev account)
client_id = "Client Id for the application"
client_secret = "Client secret for the application"

# authentication
auth.get_token(client_id=client_id, client_secret=client_secret)

# get all accounts connected to your api keys; returns json object
response = rmapi.get_all_accounts()

# grab first account id
account_id = response['data'][0]['id']

# get all the brands associated with that account; returns json object
brands_json = rmapi.get_all_brands(account_id=account_id)

# print all the brands information associated with that account id
print(json.dumps(brands_json['data'], indent=4))

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)