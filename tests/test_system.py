import unittest
from datetime import datetime
from src.database.database_manager import DatabaseManager
from src.models.calendar import Calendar
from src.models.event import Event
import os

class TestCalendarSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_filepath = 'test_calendar.pkl'
        cls.db_manager = DatabaseManager(cls.db_filepath)
        cls.calendar = Calendar(cls.db_manager)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.db_filepath):
            os.remove(cls.db_filepath)

    def setUp(self):
        self.calendar.remove_all_events()

    def test_user_flow(self):
        # Passo 1: Adicionar eventos
        event1 = Event('Meeting', '01/07/2024', '10:00', '11:00', 'Work', None)
        event2 = Event('Appointment', '02/07/2024', '14:00', '15:00', 'Personal', None)
        self.calendar.add_event(event1)
        self.calendar.add_event(event2)

        # Verificar se os eventos foram adicionados
        events = self.calendar.list_all_events()
        self.assertEqual(len(events), 2)
        self.assertEqual(events.iloc[0]['name'], 'Meeting')
        self.assertEqual(events.iloc[1]['name'], 'Appointment')

        # Passo 2: Editar um evento
        changes = {'name': 'Team Meeting', 'start_time': '09:00'}
        self.calendar.edit_event('Meeting', datetime.strptime('01/07/2024', '%d/%m/%Y'), changes)

        # Verificar se o evento foi editado
        events = self.calendar.list_all_events()
        self.assertEqual(events.iloc[0]['name'], 'Team Meeting')
        self.assertEqual(events.iloc[0]['start_time'], '09:00')

        # Passo 3: Listar eventos por data específica
        events_on_date = self.calendar.list_events_date('02/07/2024')
        self.assertEqual(len(events_on_date), 1)
        self.assertEqual(events_on_date.iloc[0]['name'], 'Appointment')

        # Passo 4: Remover um evento por nome
        self.calendar.remove_event_by_name('Team Meeting')

        # Verificar se o evento foi removido
        events = self.calendar.list_all_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events.iloc[0]['name'], 'Appointment')