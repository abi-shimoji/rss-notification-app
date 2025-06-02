from dataclasses import dataclass
from enum import IntEnum
import os
import requests
from rss.models import Article
from storage.parameter_store import get_parameter_store
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dataclasses import dataclass

class RssLogInfoIndex(IntEnum):
    name = 0
    title = 1

@dataclass
class RssLogInfo:
    name: str
    title: str

def has_been_registered(service_name: str, article: Article) -> bool:
    """
    過去に投稿しているか確認する
    
    Parameters
    ----------
    service_name: str
        RSSのサービス名
    article : Article
        投稿する記事
    
    Returns
    -------
    result : bool
        True: 投稿済み
        False: 未投稿
    """
    api_key = get_parameter_store(os.getenv("SPREADSHEET_API_KEY"))
    spreadsheet_id = os.getenv("SPREADSHEET_LOG_ID")
    api_url = os.getenv("SPREADSHEET_API_URL")
    range = "1"
    url = f"{api_url}/{spreadsheet_id}/values/{range}?key={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        for row in response.json().get('values', []):
            if row[RssLogInfoIndex.name] == service_name and row[RssLogInfoIndex.title] == article.title:
                return True
    else:
        raise Exception("投稿済みチェック", response.status_code, response.text)
    
    return False

def register_article(service_name: str, article: Article):
    """
    slackに投稿した記事をスプレッドシートに登録する。
    
    Parameters
    ----------
    service_name : str
        RSSのサービス名
    article : Article
        投稿した記事
    """
    # サービスアカウントJSONファイルのパス（環境変数 or 固定パス）
    service_account_file = "cosmic-tensor-447406-j1-c56d9528bcd6.json"
    
    # スプレッドシートIDと書き込み範囲
    spreadsheet_id = os.getenv("SPREADSHEET_LOG_ID")
    range_name = "1!A:B"

    # OAuth認証
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    service = build("sheets", "v4", credentials=credentials)

    # 書き込むデータ
    values = [[service_name, article.title]]
    body = {"values": values}

    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        updated = result.get("updates", {}).get("updatedCells", 0)
        print(f"記事をスプレッドシートに登録しました: {article.title}（{updated}セル）")

    except Exception as e:
        print("スプレッドシートへの登録に失敗しました:", e)