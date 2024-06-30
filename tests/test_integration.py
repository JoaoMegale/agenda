import unittest
from datetime import datetime
from src.database.database_manager import DatabaseManager
from src.models.calendar import Calendar
from src.models.event import Event
import os

class TestCalendarDataPersistence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_filepath = 'test_calendar_persistence.pkl'
        cls.db_manager = DatabaseManager(cls.db_filepath)
        cls.calendar = Calendar(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_filepath):
            os.remove(cls.db_filepath)

    def setUp(self):
        self.calendar.remove_all_events()

    def test_data_persistence_after_restart(self):
        event1 = Event('Conference', '01/07/2024', '09:00', '17:00', 'Work', None)
        event2 = Event('Lunch', '02/07/2024', '12:00', '13:00', 'Personal', None)
        self.calendar.add_event(event1)
        self.calendar.add_event(event2)

        # Reiniciar a sessão
        self.calendar = Calendar(self.db_manager)

        # Verificar se os eventos persistem após reinício
        events = self.calendar.list_all_events()
        self.assertEqual(len(events), 2)
        self.assertEqual(events.iloc[0]['name'], 'Conference')
        self.assertEqual(events.iloc[1]['name'], 'Lunch')

class TestCalendarEventInterval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_filepath = 'test_calendar_interval.pkl'
        cls.db_manager = DatabaseManager(cls.db_filepath)
        cls.calendar = Calendar(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_filepath):
            os.remove(cls.db_filepath)

    def setUp(self):
        self.calendar.remove_all_events()

    def test_list_events_interval(self):
        event1 = Event('Meeting', '01/07/2024', '10:00', '11:00', 'Work', None)
        event2 = Event('Doctor', '03/07/2024', '09:00', '10:00', 'Health', None)
        event3 = Event('Dinner', '05/07/2024', '20:00', '21:00', 'Personal', None)
        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)

        events = self.calendar.list_events_interval('01/07/2024', '04/07/2024')
        self.assertEqual(len(events), 2)
        self.assertEqual(events.iloc[0]['name'], 'Meeting')
        self.assertEqual(events.iloc[1]['name'], 'Doctor')

class TestCalendarCategoryModification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_filepath = 'test_calendar_category.pkl'
        cls.db_manager = DatabaseManager(cls.db_filepath)
        cls.calendar = Calendar(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_filepath):
            os.remove(cls.db_filepath)

    def setUp(self):
        self.calendar.remove_all_events()

    def test_modify_all_events_in_category(self):
        event1 = Event('Team Meeting', '01/07/2024', '10:00', '11:00', 'Work', None)
        event2 = Event('Project Review', '02/07/2024', '14:00', '15:00', 'Work', None)
        self.calendar.add_event(event1)
        self.calendar.add_event(event2)

        changes = {'category': 'Corporate'}
        self.calendar.edit_events_by_name('Team Meeting', changes)
        self.calendar.edit_events_by_name('Project Review', changes)

        events = self.calendar.list_events_category('Corporate')
        self.assertEqual(len(events), 2)
        self.assertTrue(all(events['category'] == 'Corporate'))

class TestCalendarEventListing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_filepath = 'test_calendar_listing.pkl'
        cls.db_manager = DatabaseManager(cls.db_filepath)
        cls.calendar = Calendar(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_filepath):
            os.remove(cls.db_filepath)

    def setUp(self):
        self.calendar.remove_all_events()

    def test_add_and_list_events(self):
        # Adicionar eventos
        event1 = Event('Workshop', '10/07/2024', '09:00', '12:00', 'Education', None)
        event2 = Event('Doctor Appointment', '10/07/2024', '14:00', '15:00', 'Health', None)
        event3 = Event('Conference', '11/07/2024', '10:00', '16:00', 'Work', None)
        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)

        # Listar eventos em uma data específica
        events_on_date = self.calendar.list_events_date('10/07/2024')
        self.assertEqual(len(events_on_date), 2)
        self.assertEqual(events_on_date.iloc[0]['name'], 'Workshop')
        self.assertEqual(events_on_date.iloc[1]['name'], 'Doctor Appointment')

        # Listar eventos por categoria
        health_events = self.calendar.list_events_category('Health')
        self.assertEqual(len(health_events), 1)
        self.assertEqual(health_events.iloc[0]['name'], 'Doctor Appointment')

if __name__ == "__main__":
    unittest.main()