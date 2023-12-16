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
from datetime import datetime
from dateutil import tz


_LATITUDE = "51.053822"
_LONGITUDE = "3.722270"
_METEOMATICS_BASE_URL="https://api.meteomatics.com"
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


def _construct_url(dt: datetime, weather_params: list, location: str) -> str:
    dt_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"{_METEOMATICS_BASE_URL}/{dt_str}/{','.join(weather_params)}/{location}/json"
    return url


def main() -> None:
    load_dotenv()
    access_token = _get_access_token(_METEOMATICS_TOKEN_URL)
    weather_params = ["t_2m:C"]
    location = f"{_LATITUDE},{_LONGITUDE}"
    url = _construct_url(datetime.now(tz=tz.UTC), weather_params, location)
    response = requests.get(url, {"access_token": access_token})
    print(response.text)


if __name__ == "__main__":
    main()