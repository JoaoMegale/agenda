import unittest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.models.calendar import Calendar
from src.models.event import Event

class TestCalendar(unittest.TestCase):
    
    def setUp(self):
        self.mock_db_manager = MagicMock()
        self.mock_db_manager.load_data.return_value = pd.DataFrame(columns=['name', 'date', 'start_time', 'end_time', 'category'])
        self.calendar = Calendar(self.mock_db_manager)

    def test_add_unique_event(self):
        event = Event("Event", datetime(2023, 5, 20), "10:00", "11:00", "Work")

        self.calendar.add_event(event)

        self.assertEqual(len(self.calendar.df), 1)
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Event")

    def test_add_recurrent_event_by_number_of_occurrences(self):
        event = Event("Evento Diario", datetime(2023, 1, 1), recurrence="daily")

        self.calendar.add_recurrent_event_by_num_occurrences(event, 3)

        # Primeira ocorrencia
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Evento Diario")
        self.assertEqual(self.calendar.df.iloc[0]['date'].date(), (datetime(2023, 1, 1)).date())
        # Segunda ocorrencia
        self.assertEqual(self.calendar.df.iloc[1]['name'], "Evento Diario")
        self.assertEqual(self.calendar.df.iloc[1]['date'].date(), (datetime(2023, 1, 2)).date())
        # Terceira ocorrencia
        self.assertEqual(self.calendar.df.iloc[2]['name'], "Evento Diario")
        self.assertEqual(self.calendar.df.iloc[2]['date'].date(), (datetime(2023, 1, 3)).date())

    def test_add_recurrent_event_with_invalid_number_of_occurrences(self):
        event = Event("Event", datetime(2024, 1, 1), recurrence="daily")
        
        with self.assertRaises(ValueError) as context:
            self.calendar.add_recurrent_event_by_num_occurrences(event, -1)
        self.assertTrue("Número de ocorrências inválido" in str(context.exception))

    def test_add_recurrent_event_by_end_date(self):
        event = Event("Evento Diario", datetime(2023, 1, 1), recurrence="daily")

        self.calendar.add_recurrent_event_by_end_date(event, "03/01/2023")

        # Primeira ocorrencia
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Evento Diario")
        self.assertEqual(self.calendar.df.iloc[0]['date'].date(), (datetime(2023, 1, 1)).date())
        # Segunda ocorrencia
        self.assertEqual(self.calendar.df.iloc[1]['name'], "Evento Diario")
        self.assertEqual(self.calendar.df.iloc[1]['date'].date(), (datetime(2023, 1, 2)).date())
        # Terceira ocorrencia
        self.assertEqual(self.calendar.df.iloc[2]['name'], "Evento Diario")
        self.assertEqual(self.calendar.df.iloc[2]['date'].date(), (datetime(2023, 1, 3)).date())

    def test_add_recurrent_event_with_invalid_end_date(self):
        
        event = Event("Event", "20/05/2024", "14:00", "15:00", "Work", "daily")
        invalid_end_date = "32/05/2024"

        with self.assertRaises(ValueError) as context:
            self.calendar.add_recurrent_event_by_end_date(event, invalid_end_date)
        self.assertTrue("Data de término inválida" in str(context.exception))

    def test_add_recurrent_event_with_end_date_before_start(self):
        
        event = Event("Event", "01/01/2024", "14:00", "15:00", "Work", "daily")
        end_date = "01/01/2023"

        with self.assertRaises(ValueError) as context:
            self.calendar.add_recurrent_event_by_end_date(event, end_date)
        self.assertTrue("Data de término é anterior à data de início do evento." in str(context.exception))

    def test_add_weekly_event(self):
        event = Event("Evento Semanal", datetime(2024, 1, 1), recurrence="weekly")

        self.calendar.add_recurrent_event_by_num_occurrences(event, 2)
        
        # Primeira ocorrencia
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Evento Semanal")
        self.assertEqual(self.calendar.df.iloc[0]['date'].date(), (datetime(2024, 1, 1)).date())
        # Segunda ocorrencia
        self.assertEqual(self.calendar.df.iloc[1]['name'], "Evento Semanal")
        self.assertEqual(self.calendar.df.iloc[1]['date'].date(), (datetime(2024, 1, 8)).date())

    def test_add_monthly_event(self):
        event = Event("Evento Mensal", datetime(2024, 1, 1), recurrence="monthly")

        self.calendar.add_recurrent_event_by_num_occurrences(event, 2)

        # Primeira ocorrencia
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Evento Mensal")
        self.assertEqual(self.calendar.df.iloc[0]['date'].date(), (datetime(2024, 1, 1)).date())
        # Segunda ocorrencia
        self.assertEqual(self.calendar.df.iloc[1]['name'], "Evento Mensal")
        self.assertEqual(self.calendar.df.iloc[1]['date'].date(), (datetime(2024, 2, 1)).date())

    def test_add_monthly_event_on_31st(self):
        event = Event("Evento Mensal", datetime(2024, 1, 31), recurrence="monthly")

        self.calendar.add_recurrent_event_by_num_occurrences(event, 2)

        # Primeira ocorrencia
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Evento Mensal")
        self.assertEqual(self.calendar.df.iloc[0]['date'].date(), (datetime(2024, 1, 31)).date())
        # Segunda ocorrencia
        self.assertEqual(self.calendar.df.iloc[1]['name'], "Evento Mensal")
        self.assertEqual(self.calendar.df.iloc[1]['date'].date(), (datetime(2024, 3, 31)).date())
    
    def test_add_annual_event(self):
        event = Event("Evento Anual", datetime(2024, 1, 1), recurrence="yearly")

        self.calendar.add_recurrent_event_by_num_occurrences(event, 2)
        
        # Primeira ocorrencia
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Evento Anual")
        self.assertEqual(self.calendar.df.iloc[0]['date'].date(), (datetime(2024, 1, 1)).date())
        # Segunda ocorrencia
        self.assertEqual(self.calendar.df.iloc[1]['name'], "Evento Anual")
        self.assertEqual(self.calendar.df.iloc[1]['date'].date(), (datetime(2025, 1, 1)).date())

    def test_add_event_with_optional_fields_empty(self):
        event = Event("Event", datetime(2023, 6, 15), "10:00", "11:00", "")

        self.calendar.add_event(event)

        self.assertEqual(len(self.calendar.df), 1)
        self.assertEqual(self.calendar.df.iloc[0]['category'], '')

    def test_remove_all_events(self):
        event1 = Event("Event 1", datetime(2023, 5, 20), "10:00", "11:00")
        event2 = Event("Event 2", datetime(2023, 5, 21), "12:00", "13:00")

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.remove_all_events()

        self.assertEqual(len(self.calendar.df), 0)

    def test_remove_event_by_name_and_date(self):
        event = Event("Event to Remove", datetime(2023, 5, 20), "10:00", "11:00")

        self.calendar.add_event(event)
        self.calendar.remove_event_by_name_and_date("Event to Remove", "20/05/2023")

        self.assertEqual(len(self.calendar.df), 0)

    def test_remove_event_by_name(self):
        event1 = Event("Event", datetime(2023, 5, 20), "10:00", "11:00")
        event2 = Event("Event", datetime(2023, 5, 21), "12:00", "13:00")
        event3 = Event("Other", datetime(2023, 5, 22), "10:00", "11:00")

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)
        self.calendar.remove_event_by_name("Event")

        self.assertEqual(len(self.calendar.df), 1)
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Other")

    def test_remove_event_by_nonexisting_name(self):
        event1 = Event("Event", datetime(2023, 5, 20), "10:00", "11:00")
        event2 = Event("Meeting", datetime(2023, 5, 21), "12:00", "13:00")

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.remove_event_by_name("Random-name")

        self.assertEqual(len(self.calendar.df), 2)

    def test_list_all_events(self):
        event1 = Event("Evento1", datetime(2020, 1, 1))
        event2 = Event("Evento2", datetime(2024, 5, 5), category="Cat1")

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        all_events = self.calendar.list_all_events()

        self.assertEqual(len(all_events), 2)

    def test_list_all_events_when_result_is_empty(self):
        all_events = self.calendar.list_all_events()

        self.assertEqual(all_events, "Nenhum evento cadastrado.")

    def test_list_events_today(self):
        today = datetime.now().date()
        event = Event("Evento hoje", today)

        self.calendar.add_event(event)
        events_today = self.calendar.list_events_today()

        self.assertEqual(len(events_today), 1)
        
    def test_list_events_today_when_result_is_empty(self):
        events_today = self.calendar.list_events_today()

        self.assertEqual(events_today, "Nenhum evento para hoje.")

    def test_list_events_of_date(self):
        specific_date = datetime(2023, 5, 20)
        event = Event("Date Event", specific_date)
        other_date = datetime(2024, 1, 1)
        other_event = Event("Other Event", other_date)

        self.calendar.add_event(event)
        self.calendar.add_event(other_event)
        events = self.calendar.list_events_date("20/05/2023")

        self.assertEqual(len(events), 1)
        self.assertEqual(events.iloc[0]['name'], "Date Event")

    def test_list_events_of_date_when_result_is_empty(self):
        specific_date = "01/01/2024"
        events_date = self.calendar.list_events_date(specific_date)

        self.assertEqual(events_date, "Nenhum evento para a data.")

    def test_list_events_of_invalid_date(self):
        invalid_date = "32/01/2024"

        with self.assertRaises(ValueError) as context:
            self.calendar.list_events_date(invalid_date)

        self.assertTrue("Data inválida." in str(context.exception))

    def test_list_events_until_date(self):
        today = datetime.now().date()
        event_today = Event("Event today", today)

        tomorrow = today + timedelta(days=1)
        event_tomorrow = Event("Event tomorrow", tomorrow)

        next_week = today + timedelta(days=7)
        event_next_week = Event("Event next week", next_week)

        self.calendar.add_event(event_today)
        self.calendar.add_event(event_tomorrow)
        self.calendar.add_event(event_next_week)

        events = self.calendar.list_events_until_date(tomorrow)

        self.assertEqual(len(events), 2)
        self.assertEqual(events.iloc[0]['name'], "Event today")
        self.assertEqual(events.iloc[1]['name'], "Event tomorrow")

    def test_list_events_until_date_when_result_is_empty(self):
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        event_next_week = Event("Event next week", next_week)

        self.calendar.add_event(event_next_week)

        events = self.calendar.list_events_until_date(tomorrow)

        self.assertEqual(events, "Nenhum evento para o período.")

    def test_list_events_until_invalid_date(self):
        invalid_date = "32/01/2024"

        with self.assertRaises(ValueError) as context:
            self.calendar.list_events_until_date(invalid_date)

        self.assertTrue("Data inválida." in str(context.exception))

    def test_list_events_until_date_before_today(self):
        today = datetime.now().date()
        yesterday = today - timedelta(days = 1)

        events = self.calendar.list_events_until_date(yesterday)

        self.assertEqual(events, "A data fornecida é anterior a hoje.")

    def test_list_events_in_time_interval(self):
        event1 = Event("event 1", datetime(2024, 1, 1))
        event2 = Event("event 2", datetime(2024, 3, 1))
        event3 = Event("event 3", datetime(2024, 5, 1))

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)

        events = self.calendar.list_events_interval("05/01/2024", "01/04/2024")

        self.assertEqual(len(events), 1)

    def test_list_events_in_time_interval_with_evens_in_border(self):
        event1 = Event("event 1", datetime(2024, 1, 1))
        event2 = Event("event 2", datetime(2024, 3, 1))
        event3 = Event("event 3", datetime(2024, 5, 1))

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)

        events = self.calendar.list_events_interval("01/01/2024", "01/05/2024")

        self.assertEqual(len(events), 3)

    def test_list_events_in_time_interval_when_result_is_empty(self):
        event_out = Event("event", datetime(2024, 1, 1))

        self.calendar.add_event(event_out)
        events = self.calendar.list_events_interval("01/05/2024", "01/06/2024")

        self.assertEqual(events, "Nenhum evento para o período.")

    def test_list_events_in_time_interval_with_end_before_start(self):
        start_date = "05/01/2024"
        end_date = "01/01/2024"

        events = self.calendar.list_events_interval(start_date=start_date, end_date=end_date)

        self.assertEqual(events, "A data de fim é anterior à de início.")

    def test_list_events_in_time_intervale_with_invalid_start_date(self):
        start_date = "32/01/2023"
        end_date = "01/01/2024"

        with self.assertRaises(ValueError) as context:
            self.calendar.list_events_interval(start_date, end_date)

        self.assertTrue("Data de início inválida" in str(context.exception))

    def test_list_events_in_time_intervale_with_invalid_end_date(self):
        start_date = "01/01/2023"
        end_date = "41/01/2024"

        with self.assertRaises(ValueError) as context:
            self.calendar.list_events_interval(start_date, end_date)

        self.assertTrue("Data de fim inválida" in str(context.exception))

    def test_list_events_by_category(self):
        event1 = Event("Category Event", datetime(2023, 5, 20), "10:00", "11:00", "Specific Category")
        event2 = Event("Other Event", datetime(2023, 5, 20), "10:00", "11:00", "Another Category")

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)

        events = self.calendar.list_events_category("Specific Category")

        self.assertEqual(len(events), 1)
        self.assertEqual(events.iloc[0]['category'], "Specific Category")

    def test_list_events_by_category_when_result_is_empty(self):
        event1 = Event("Category Event", datetime(2023, 5, 20), "10:00", "11:00", "Specific Category")
        event2 = Event("Other Event", datetime(2023, 5, 20), "10:00", "11:00", "Another Category")

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)

        events = self.calendar.list_events_category("Third Category")

        self.assertEqual(events, "Nenhum evento para a categoria.")

    def test_search_events_by_term(self):
        event1 = Event("Event", datetime(2024, 1, 1))
        event2 = Event("Evemto", datetime(2024, 1, 1))
        event3 = Event("Other", datetime(2024, 1, 1))

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)

        events = self.calendar.find_events_by_name("Eve")

        self.assertEqual(len(events), 2)

    def test_search_events_by_term_case_insensitive(self):
        event1 = Event("Event", datetime(2024, 1, 1))
        event2 = Event("Evemt", datetime(2024, 1, 1))
        event3 = Event("Other", datetime(2024, 1, 1))

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)

        events = self.calendar.find_events_by_name("eve")

        self.assertEqual(len(events), 2)

    def test_search_events_by_term_when_result_is_empty(self):
        event = Event("evento", datetime(2024, 1, 1))
        self.calendar.add_event(event)

        events = self.calendar.find_events_by_name("another")

        self.assertEqual(events, "Nenhum evento com este nome.")

    def test_search_events_by_empty_term(self):
        
        events = self.calendar.find_events_by_name("")
        
        self.assertEqual(events, "O termo deve conter pelo menos 1 caractere.")

    def test_list_categories(self):
        event1 = Event("Event", datetime(2024, 1, 1), category="cat1")
        event2 = Event("Event2", datetime(2024, 1, 1), category="cat2")

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)

        categories = self.calendar.list_categories()

        self.assertListEqual(categories, ["cat1", "cat2"])

    def test_list_categories_with_none_category(self):
        event1 = Event("Event", datetime(2024, 1, 1), category="cat1")
        event2 = Event("Event2", datetime(2024, 1, 1), category="cat2")
        event3 = Event("Event3", datetime(2024, 1, 1))

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)

        categories = self.calendar.list_categories()

        self.assertListEqual(categories, ["cat1", "cat2"])

    def test_edit_single_event_by_name(self):
        event = Event("Event", datetime(2023, 6, 15), "10:00", "11:00", "Category")

        self.calendar.add_event(event)
        self.calendar.edit_events_by_name("Event", {"name": "Edited Event"})

        self.assertEqual(self.calendar.df.iloc[0]['name'], "Edited Event")

    def test_edit_multiple_events_by_name(self):
        event1 = Event("Event", datetime(2023, 6, 15), "10:00", "11:00", "Category")
        event2 = Event("Event", datetime(2023, 6, 15), "10:00", "11:00", "Category")
        event3 = Event("Other", datetime(2023, 10, 15), "10:00", "11:00", "Category")

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)
        self.calendar.edit_events_by_name("Event", {"name": "Edited Event"})

        self.assertEqual(self.calendar.df.iloc[0]['name'], "Edited Event")
        self.assertEqual(self.calendar.df.iloc[1]['name'], "Edited Event")
        self.assertEqual(self.calendar.df.iloc[2]['name'], "Other")

    def test_edit_event_by_name_and_date(self):
        event = Event("Event", datetime(2023, 6, 15), "10:00", "11:00", "Category")
        event2 = Event("Other name", datetime(2023, 6, 15), "11:00", "12:00", "Category")
        event3 = Event("Event", datetime(2023, 7, 15), "10:00", "11:00", "Category")

        self.calendar.add_event(event)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)
        self.calendar.edit_event("Event", datetime(2023, 6, 15), {"name": "Specific Edited Event"})
        
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Specific Edited Event")

    def test_edit_nonexistent_event(self):
        event = Event("Event", datetime(2023, 6, 15), "10:00", "11:00", "Category")

        self.calendar.add_event(event)
        self.calendar.edit_events_by_name("Other Event", {"name": "Edited Event"})

        self.assertEqual(len(self.calendar.df), 1)
        self.assertEqual(self.calendar.df.iloc[0]['name'], "Event")

if __name__ == '__main__':
    unittest.main()