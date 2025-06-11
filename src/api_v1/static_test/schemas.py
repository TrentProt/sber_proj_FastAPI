from typing import List, Union

from pydantic import BaseModel

class QAnswer(BaseModel):
    q_num: int
    answer_id: Union[int, None] = None

class AddAttemptUser(BaseModel):
    time_execution: int
    qanswers: List[QAnswer]