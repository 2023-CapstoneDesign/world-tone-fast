from pydantic import BaseModel
from typing import List

class Script(BaseModel):
    start_time: tuple
    end_time: tuple
    text: str

    def duration(self):
        return self.end_time - self.start_time

    def __str__(self):
        return f"{self.start_time} --> {self.end_time}\n{self.text}"
