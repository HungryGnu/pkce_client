from typing import List, Union
from .token_config_map import TokenConfigMap
from pathlib import Path
import os
import json

class PkceLoginConfig():
    def __init__(self, authorization_uri: str, token_uri: str, scopes: List[str], client_id: str, internal_port: int, 
        add_random_state: bool, random_state_length: int = 0, verify_authorization_server_https: bool = True,
        redirect_uri_extension: str = "", token_config_map: Union[TokenConfigMap, None] = None) -> None:
        """Initializes the configuration for PKCE sign in.

        Args:
            authorization_uri (str): The URL for the OAuth2 Authorization endpoint.
            token_uri (str): The URL for the OAuth2 Token endpoint.
            scopes (List[str]): The list of scopes to request.
            client_id (str): The ID of the client to use.
            internal_port (int): The TCP port to listen for responses from the server.
            add_random_state (bool): Whether to add a random state to the Code request.
            random_state_length (int, optional): The length of the random state created when enabled. Defaults to 0.
            verify_authorization_server_https (bool, optional): Whether to verify the HTTPs connection to the server. Defaults to True.
            redirect_uri_extension (str, optional): An optional suffix to add to the redirect URI, such as /callback. Defaults to "".
            token_config_map (TokenConfigMap, optional): An optional map to edit how the token is mapped into a PkceToken. Defaults to None.

        Raises:
            ValueError: The authorization_uri is None or empty.
            ValueError: The token_uri is None or empty.
            ValueError: The client_id is None or empty.
            ValueError: The internal_port is not a valid port number.
            ValueError: The redirect_uri is an absolute uri.
        """

        if not authorization_uri or authorization_uri == "":
            raise ValueError("An authorization_uri is required")

        if not token_uri or token_uri == "":
            raise ValueError("A token_uri is required")

        if not scopes or len(scopes) < 1:
            scopes = []

        if not client_id or client_id == "":
            raise ValueError("A client_id is required")

        if not internal_port or internal_port < 1 or internal_port > 65535:
            raise ValueError("A valid port is required, normally between 1024 and 65535, such as 8080")
        
        if redirect_uri_extension:
            if redirect_uri_extension.startswith("http:"):
                raise ValueError("The redirect_uri must be a relative uri (such as /callback for http://localhost/callback)")
            elif redirect_uri_extension.startswith("/"):
                redirect_uri_extension = redirect_uri_extension.removeprefix("/")
        else:
            redirect_uri_extension = ""

        if token_config_map is None:
            token_config_map = TokenConfigMap()
        
        self.authorization_uri = authorization_uri
        self.token_uri = token_uri
        self.scopes = scopes
        self.client_id = client_id
        self.internal_port = internal_port
        self.verify_authorization_server_https = verify_authorization_server_https
        self.add_random_state = add_random_state
        self.random_state_length = random_state_length
        self.redirect_uri_extension = redirect_uri_extension
        self.token_config_map = token_config_map

    @classmethod
    def from_config_file(cls, path):
        file_path = Path(os.path.abspath(os.path.expanduser(path)))
        # handle file that doesn't exist
        if not os.path.exists(file_path):
            raise ValueError(f'Unable to locate: {file_path}')
        with open(file_path, 'rb') as f:
            doc = json.load(f)
        tkm = TokenConfigMap(**doc["pkce_token_map"])
        return cls(**doc["pkce_login"], token_config_map=tkm)
        
    