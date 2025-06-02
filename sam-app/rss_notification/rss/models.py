from dataclasses import dataclass
from typing import List

@dataclass
class RssInfo:
    name: str
    type: str
    endpoint: str

@dataclass
class Article:
    title: str
    description: str
    link: str
    date: str
