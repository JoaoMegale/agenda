from datetime import datetime

class Event:
    def __init__(self, name, date, start_time=None, end_time=None, category=None, recurrence=None):
        self.name = name
        self.date = datetime.strptime(date, '%d/%m/%Y') if isinstance(date, str) else date
        self.start_time = start_time
        self.end_time = end_time
        self.category = category
        self.recurrence = recurrence

    def to_dict(self):
        return {
            'name': self.name,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'category': self.category
        }