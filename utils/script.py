from pydantic import BaseModel
from datetime import datetime, time

class Script(BaseModel):
    start_time: time
    end_time: time
    text: str

    def duration_self(self):
        dt_st = datetime.combine(datetime.today(), self.start_time)
        dt_et = datetime.combine(datetime.today(), self.end_time)
        difference = int((dt_et - dt_st).total_seconds() * 1000)
        return difference

    def duration_other(self, other):
        dt_st = datetime.combine(datetime.today(), other.start_time)
        dt_et = datetime.combine(datetime.today(), self.end_time)
        difference = int((dt_st - dt_et).total_seconds() * 1000)
        return difference

    def __str__(self):
        return f"{self.start_time} --> {self.end_time}\n{self.text}"
