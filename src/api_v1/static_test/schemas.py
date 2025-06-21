from typing import List, Union

from pydantic import BaseModel


class OkStatus(BaseModel):
    ok: bool
    message: str


class AnswersSchema(BaseModel):
    id: int
    answer_text: str


class GetQuestionSchema(BaseModel):
    q_num: int
    question_text: str
    answers: List[AnswersSchema]


class TestPassed(OkStatus):
    test_was_passed: bool


class UserAnswerSchema(BaseModel):
    id: int
    answer_text: str


class CorrectAnswerSchema(BaseModel):
    id: int
    correct_answer_text: str


class ResultAnswersUserSchema(BaseModel):
    q_num: int
    question_text: str
    user_answer: UserAnswerSchema
    is_correct: bool
    correct_answer: CorrectAnswerSchema


class ResultTestSchema(BaseModel):
    test_id: int
    count_correct_answer: int
    count_question: int
    score: int
    time_execution: int
    data_answers: List[ResultAnswersUserSchema]