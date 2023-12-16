"""
This module implements functionality to request weather information from the 
API provided by meteomatics.

The pattern of the URL:

api.meteomatics.com/validdatetime/parameters/locations/format?optionals
"""


import os
import requests
from typing import Union
from dotenv import load_dotenv


_METEOMATICS_BASE_URL="https://api.meteomatics.com/2023-12-16T00:00:00Z/t_2m:C/52.520551,13.461804/html"
_METEOMATICS_TOKEN_URL="https://login.meteomatics.com/api/v1/token"


def _get_access_token(token_url: str) -> Union[str, None]:
    """
    This function returns an access token used to make API calls.

    Args:
        token_url (str): base URL to make API call.

    Returns:
        Union[str, None]: access token if the request is successful, otherwise 
            None.
    """
    username = os.getenv("_METEOMATICS_USERNAME")
    password = os.getenv("_METEOMATICS_PASSWORD")
    response = requests.get(_METEOMATICS_TOKEN_URL, auth=(username, password))
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def main() -> None:
    load_dotenv()
    access_token = _get_access_token(_METEOMATICS_TOKEN_URL)
    response = requests.get(
        _METEOMATICS_BASE_URL, {"access_token": access_token})
    print(response)


if __name__ == "__main__":
    main()