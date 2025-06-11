from pydantic import BaseModel

from typing import List, Union


class SectionTopicOutForTopic(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    test_count: int
    solved_count: int



class TopicsOut(BaseModel):
    id: int
    name: str



class Tests(BaseModel):
    id: int
    title: str
    type_test: Union[str, None]
    description: str
    status: bool
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