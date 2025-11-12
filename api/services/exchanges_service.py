import os
import requests

from api.utils.response_wrapper import api_response
from api.utils.constants import Constants

EXTERNAL_EXCHANGE = os.getenv("EXTERNAL_EXCHANGES")

if not EXTERNAL_EXCHANGE:
    raise ValueError("No DATABASE_URL environment variable set")


def get_global_exchanges():
    try:
        response = requests.get(EXTERNAL_EXCHANGE)
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            return api_response(data=data["rates"], detail="Exchanges found", status_code=200)
        else:
            raise api_response(data={"USD": Constants.DEFAULT_TAX}, status_code=response.status_code, detail=f"Error consultando la API: {response.reason}")
    except Exception as e:
        raise e