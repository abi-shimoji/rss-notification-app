import os
import requests
from urllib.parse import quote

aws_session_token = os.environ.get('AWS_SESSION_TOKEN')

def get_parameter_store(name: str) -> str:
    """
    Parameter Storeから値を取得する

    Parameters
    ----------
    name : str
        取得したいパラメータ名

    Returns
    -------
    value : str
        パラメータの値
    """
    headers = { "X-Aws-Parameters-Secrets-Token": aws_session_token }
    encoded_name = quote(name, safe='')
    endpoint = f"http://localhost:2773/systemsmanager/parameters/get?name={encoded_name}&withDecryption=true"

    response = requests.get(url=endpoint, headers=headers)
    value = response.json().get("Parameter", {}).get("Value")

    if value is None:
        raise ValueError(f"Parameter '{name}' の値が取得できませんでした")

    return value
