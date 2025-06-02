import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
from .models import Article
from .models import RssInfo
from storage.registry import has_been_registered, register_article

def get_rss(rss_info: RssInfo) -> List[Article]:
    """
    RSSの内容を取得する
    
    Parameters
    ----------
    url : str
        RSSのエンドポイント
        
    Returns
    -------
    articles : Article
        投稿する記事一覧
    """
    articles: List[Article] = []
    feed = feedparser.parse(rss_info.endpoint)

    for entry in feed.entries:
        description_text = BeautifulSoup(entry.description, "html.parser").get_text()
        description = description_text[:100] + "..."
        pub_date = getattr(entry, 'published', None)

        pub_date_str = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d') if pub_date else '不明'
        article = Article(
            title=entry.title,
            description=description,
            link=entry.link,
            date=pub_date_str
        )
        if not has_been_registered(rss_info.name, article):
            articles.append(article)
            register_article(rss_info.name,article)

    return articles
