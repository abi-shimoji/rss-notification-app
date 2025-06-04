from dataclasses import dataclass

@dataclass
class Article:
    title: str
    description: str
    link: str
    date: str

def register_article(service_name: str, article: Article):
    """
    slackに投稿した記事を登録する。
    
    Parameters
    ----------
    service_name : str
        RSSのサービス名
    article : Article
        投稿した記事
    """
    print('hello')


def lambda_handler(event, context):
    print("hello")
