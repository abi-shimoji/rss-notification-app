import json
import os
import requests
from dataclasses import asdict, dataclass
from typing import List
from rss.models import Article
from storage.parameter_store import get_parameter_store

@dataclass
class SlackMessageField:
    title: str
    value: str

@dataclass
class SlackMessageAttachment:
    fallback: str
    text: str
    color: str
    fields: List[SlackMessageField]

def send_slack(title: str, articles: List[Article]):
    """
    取得した記事をslackに投稿する
    
    Parameters
    ----------
    articles : Article
        投稿する記事一覧
    """
    attachments = []

    for article in articles:
        message_field = SlackMessageField(
            title=title,
            value=f"内容 : {article.description}\nリンク : {article.link}\n投稿日時 : {article.date}"
        )
        attachment = SlackMessageAttachment(
            fallback=article.title,
            text=f"*タイトル : {article.title}*\n",
            color="#00FF00",
            fields=[message_field]
        )
        attachments.append(asdict(attachment))

    payload = { "attachments": attachments }

    response = requests.post(
        get_parameter_store(os.getenv("SLACK_ENDPOINT")),
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    if response.status_code != 200:
        raise Exception("Slack送信エラー")
