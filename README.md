# Python PKCE Client

This python package contains a simple client to request tokens using the OAuth 2/OIDC Authorization Code PKCE flow.

## Sample usage

```python
from pkce_client import PkceClient, PkceLoginConfig

config = PkceLoginConfig(
    authorization_uri="https://localhost:44300/connect/authorize",
    token_uri="https://localhost:44300/connect/token",
    scopes=[ "openid", "profile", "api" ],
    client_id="python-nb",
    internal_port=4444,
    add_random_state=True,
    random_state_length=32,
    verify_authorization_server_https=False
)

login_client = PkceClient(config)
pkce_token = login_client.login()
headers = { "Authorization": "Bearer " + str(pkce_token.access_token) }
```

### Using a JSON config file

If you use a single configuration frequently it will be easier to store the config above in JSON format.

The `pkce_token_map` object allows you to override the default token map options for instance if your enpoint is 'scope' (singular) instead of 'scopes' (plural).

```json
{
  "pkce_login":{
      "authorization_uri":"<YOUR AUTH URI",
      "token_uri":"YOUR TOKEN URI",
      "scopes":[ "openid", "email", "roles" ],
      "client_id": "<CLIENT ID PROVIDED BY YOUR AUTH ADMIN>",
      "internal_port":4444,
      "add_random_state":true,
      "random_state_length":32,
      "verify_authorization_server_https":true
   },
  "pkce_token_map": {
      "token_type":"token_type",
      "expires_in":"expires_in",
      "access_token":"access_token",
      "id_token":"id_token",
      "scopes":"scope",
      "refresh_token":"refresh_token"
   }
}
```

If the config is store in `~/my_config.json`:
```python
config = PkceLoginConfig.from_config_file('~/my_config.json')

login_client = PkceClient(config)
pkce_token = login_client.login()
```