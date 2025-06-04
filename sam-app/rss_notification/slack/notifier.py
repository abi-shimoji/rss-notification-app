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

def send_slack(title: str, icon: str, articles: List[Article]):
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

@dataclass
class DiscordMessageFields:
    name: str
    value: str
    inline: bool

@dataclass
class DiscordMessageEmbeds:
    color: int
    fields: List[DiscordMessageFields]

@dataclass
class DiscordMessageBody:
    username: str
    avatar_url: str
    embeds: List[DiscordMessageEmbeds]

def send_discord(title: str, icon: str, articles: List[Article]):
    """
    取得した記事をdiscordに投稿する

    Parameters
    ----------
    articles : List[Article]
        投稿する記事一覧
    """
    discord_message_fields: List[DiscordMessageFields] = []

    for article in articles:
        discord_message_fields.append(DiscordMessageFields(
            name=article.title,
            value=f"内容 : {article.description}\nリンク : {article.link}\n投稿日時 : {article.date}",
            inline=False
        ))

    discord_message_embeds = DiscordMessageEmbeds(
        color=int("00FF00", 16),  # "#00FF00" を整数に変換
        fields=discord_message_fields
    )

    discord_message_body = DiscordMessageBody(
        username=title,
        avatar_url=icon,
        embeds=[discord_message_embeds]
    )

    response = requests.post(
        get_parameter_store(os.getenv("DISCORD_ENDPOINT")),  # DISCORD_ENDPOINT に変更するのがベスト
        headers={"Content-Type": "application/json"},
        data=json.dumps(asdict(discord_message_body))
    )

    if response.status_code != 200:
        raise Exception(f"Discord送信エラー: {response.status_code}, {response.text}")