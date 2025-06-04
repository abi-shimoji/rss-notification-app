import os
from enum import Enum
from rss.fetcher import get_rss
from slack.notifier import send_slack, send_discord
from storage.spreadsheet import get_rss_info
from storage.sqs import send_sqs

class NotificationApp(Enum):
    slack = "slack"
    discord = "discord"

def lambda_handler(event, context):
    rss_info_list = get_rss_info()
    for rss_info in rss_info_list:
        if rss_info.name == 'サイト名' and rss_info.type == '形式' and rss_info.endpoint == 'エンドポイント':
            continue
        articles = get_rss(rss_info)
        
        notification_app = os.getenv("NOTIFICATION_APP")

        if notification_app == NotificationApp.slack.value:
            print("slack")
            send_slack(rss_info.name, rss_info.icon, articles)
        elif notification_app == NotificationApp.discord.value:
            print("discord")
            send_discord(rss_info.name, rss_info.icon, articles)

        # 投稿した内容をSQSに登録する
        send_sqs()
