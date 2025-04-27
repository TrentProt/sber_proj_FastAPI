from pydantic import BaseModel

from typing import List


class SectionTopicOut(BaseModel):
    id: int
    title: str
    description: str
    tests_count: int
    solved_tests: int



class TopicOut(BaseModel):
    id: int
    name: str
    description: str
    sections_topic: List[SectionTopicOut]