import os
import requests
from typing import List
from rss.models import RssInfo
from enum import IntEnum
from storage.parameter_store import get_parameter_store

class RssInfoIndex(IntEnum):
    name = 0
    type = 1
    endpoint = 2

def get_rss_info() -> List[RssInfo]:
    """
    RSS情報を取得する
    
    Returns
    -------
    rss_info : List[RssInfo]
        RSS情報一覧
    """
    api_key = get_parameter_store(os.getenv("SPREADSHEET_API_KEY"))
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    api_url = os.getenv("SPREADSHEET_API_URL")
    range = "1"
    url = f"{api_url}/{spreadsheet_id}/values/{range}?key={api_key}"

    response = requests.get(url)
    rss_info = []

    if response.status_code == 200:
        for row in response.json().get('values', []):
            rss_info.append(RssInfo(
                name=row[RssInfoIndex.name],
                type=row[RssInfoIndex.type],
                endpoint=row[RssInfoIndex.endpoint]
            ))
    else:
        print("失敗", response.status_code, response.text)

    return rss_info
