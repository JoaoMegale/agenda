from datetime import datetime

class Event:
    def __init__(self, name, date, start_time=None, end_time=None, category=None, recurrence=None):
        self.name = name

        # Verificar data inválida
        try:
            self.date = datetime.strptime(date, '%d/%m/%Y') if isinstance(date, str) else date
        except ValueError:
            raise ValueError(f"Data inválida: {date}")

        # Verificar horários inválidos e a ordem dos horários
        if start_time:
            try:
                self.start_time = datetime.strptime(start_time, '%H:%M').time()
            except ValueError:
                raise ValueError(f"Horário de início inválido: {start_time}")
        else:
            self.start_time = None

        if end_time:
            try:
                self.end_time = datetime.strptime(end_time, '%H:%M').time()
            except ValueError:
                raise ValueError(f"Horário de fim inválido: {end_time}")
        else:
            self.end_time = None

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValueError("Horário de início não pode ser depois ou igual ao horário de fim")

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
