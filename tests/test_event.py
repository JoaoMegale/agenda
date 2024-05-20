import unittest
from datetime import datetime
from src.models.event import Event

class TestEvent(unittest.TestCase):

    def test_valid_event(self):
        event = Event("Meeting", "20/05/2024", "14:00", "15:00", "Work", "daily")
        self.assertEqual(event.name, "Meeting")
        self.assertEqual(event.date, datetime.strptime("20/05/2024", "%d/%m/%Y"))
        self.assertEqual(event.start_time, datetime.strptime("14:00", "%H:%M").time())
        self.assertEqual(event.end_time, datetime.strptime("15:00", "%H:%M").time())
        self.assertEqual(event.category, "Work")
        self.assertEqual(event.recurrence, "daily")

    def test_invalid_date(self):
        with self.assertRaises(ValueError) as context:
            Event("Invalid Date", "32/01/2024", "14:00", "15:00")
        self.assertTrue("Data inválida" in str(context.exception))

    def test_invalid_start_time(self):
        with self.assertRaises(ValueError) as context:
            Event("Invalid Start Time", "20/05/2024", "25:00", "15:00")
        self.assertTrue("Horário de início inválido" in str(context.exception))

    def test_invalid_end_time(self):
        with self.assertRaises(ValueError) as context:
            Event("Invalid End Time", "20/05/2024", "14:00", "25:00")
        self.assertTrue("Horário de fim inválido" in str(context.exception))

    def test_start_time_after_end_time(self):
        with self.assertRaises(ValueError) as context:
            Event("Start After End", "20/05/2024", "15:00", "14:00")
        self.assertTrue("Horário de início não pode ser depois ou igual ao horário de fim" in str(context.exception))

    def test_missing_end_time(self):
        event = Event("No End Time", "20/05/2024", start_time="14:00")
        self.assertEqual(event.start_time, datetime.strptime("14:00", "%H:%M").time())
        self.assertEqual(event.end_time, None)

if __name__ == "__main__":
    unittest.main()