from pydantic import BaseModel
from datetime import datetime

class Script(BaseModel):
    start_time: str
    end_time: str
    text: str

    def time_convert(self):
        self.start_time = datetime.strptime(self.start_time, "%H:%M:%S,%f").time()
        self.end_time = datetime.strptime(self.end_time, "%H:%M:%S,%f").time()

    def duration(self):
        dt_st = datetime.combine(datetime.today(), self.start_time)
        dt_et = datetime.combine(datetime.today(), self.end_time)
        return dt_et - dt_st

    def __str__(self):
        return f"{self.start_time} --> {self.end_time}\n{self.text}"
