from pydantic import BaseModel

from typing import List


class SectionTopicOutForTopic(BaseModel):
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
    sections_topic: List[SectionTopicOutForTopic]


class Tests(BaseModel):
    id: int
    title: str
    description: str
    status: str
    count_solved: int
    count_questions: int


class SectionForTests(BaseModel):
    id: int
    title: str
    description: str
    count_solved: int
    count_tests: int
    theory: str
    tests: List[Tests]