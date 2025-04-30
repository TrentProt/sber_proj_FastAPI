from pydantic import BaseModel

from typing import List


class SectionTopicOut(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    test_count: int
    solved_count: int



class TopicOut(BaseModel):
    id: int
    name: str
    description: str
    sections_topic: List[SectionTopicOut]