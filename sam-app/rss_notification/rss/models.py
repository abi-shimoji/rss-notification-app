from dataclasses import dataclass
from typing import List

@dataclass
class RssInfo:
    name: str
    type: str
    endpoint: str
    icon: str

@dataclass
class Article:
    title: str
    description: str
    link: str
    date: str
