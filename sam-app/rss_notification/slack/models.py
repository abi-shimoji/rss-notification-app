from dataclasses import dataclass
from typing import List

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
