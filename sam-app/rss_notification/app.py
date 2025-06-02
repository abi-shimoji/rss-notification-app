from rss.fetcher import get_rss
from slack.notifier import send_slack
from storage.spreadsheet import get_rss_info

def lambda_handler(event, context):
    rss_info_list = get_rss_info()
    for rss_info in rss_info_list:
        if rss_info.name == 'サイト名' and rss_info.type == '形式' and rss_info.endpoint == 'エンドポイント':
            continue
        articles = get_rss(rss_info)
        send_slack(rss_info.name, articles)
