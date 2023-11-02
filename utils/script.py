from pydantic import BaseModel
from datetime import datetime, time

class Script(BaseModel):
    start_time: time
    end_time: time
    text: str

    def duration(self):
        dt_st = datetime.combine(datetime.today(), self.start_time)
        dt_et = datetime.combine(datetime.today(), self.end_time)
        return dt_et - dt_st

    def __str__(self):
        return f"{self.start_time} --> {self.end_time}\n{self.text}"
