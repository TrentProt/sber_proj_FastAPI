from typing import List, Union

from pydantic import BaseModel


class QAnswers(BaseModel):
    q_num: int
    answer_id: Union[int, None] = None

class AddUserAttempt(BaseModel):
    time_execution: int
    # Секунды
    qanswers: List[QAnswers]
