from models.event import Event

import pandas as pd
from datetime import datetime, timedelta

class Calendar:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.df = self.db_manager.load_data()

    def add_event(self, event):
        """
        Adiciona evento ao calendário.
        """
        event_list = []
        event_list.append(event.to_dict())
        event_df = pd.DataFrame(event_list)
        self.df = pd.concat([self.df, event_df], ignore_index=True)
        self.db_manager.save_data(self.df)

    def add_recurrent_event_by_end_date(self, event, end_date):
        """
        Adiciona um evento recorrente ao calendário, até a data limite.
        """
        # Verifica se a data de fim é válida
        try:
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
        except ValueError:
            raise ValueError(f"Data de término inválida: {end_date}")

        if event.date > end_date:
            raise ValueError("Data de término é anterior à data de início do evento.")
        
        current_date = event.date
        event_list = []

        while current_date <= end_date:
            new_event = Event(event.name, current_date, event.start_time, event.end_time, event.category, event.recurrence)
            event_list.append(new_event.to_dict())
            if event.recurrence == 'daily':
                current_date += timedelta(days=1)
            elif event.recurrence == 'weekly':
                current_date += timedelta(weeks=1)
            elif event.recurrence == 'monthly':
                # Calcula o próximo mês e mantém o mesmo dia
                month_increment = (current_date.month % 12) + 1
                year_increment = current_date.year + (current_date.month // 12)
                try:
                    current_date = current_date.replace(year=year_increment, month=month_increment)
                except ValueError:
                    # Se o dia não existir no próximo mês, pule para o próximo mês válido
                    while True:
                        month_increment = (month_increment % 12) + 1
                        year_increment += (month_increment // 12)
                        try:
                            current_date = current_date.replace(year=year_increment, month=month_increment)
                            break
                        except ValueError:
                            continue
            elif event.recurrence == 'yearly':
                current_date = current_date.replace(year=current_date.year + 1)

        event_df = pd.DataFrame(event_list)
        self.df = pd.concat([self.df, event_df], ignore_index=True)
        self.db_manager.save_data(self.df)

    def add_recurrent_event_by_num_occurrences(self, event, num_occurrences):
        """
        Adiciona um evento recorrente ao calendário X vezes.
        """
        if num_occurrences < 1:
            raise ValueError(f"Número de ocorrências inválido: {num_occurrences}")

        current_date = event.date
        occurrences = 0
        event_list = []

        while occurrences < num_occurrences:
            new_event = Event(event.name, current_date, event.start_time, event.end_time, event.category, event.recurrence)
            event_list.append(new_event.to_dict())
            if event.recurrence == 'daily':
                current_date += timedelta(days=1)
            elif event.recurrence == 'weekly':
                current_date += timedelta(weeks=1)
            elif event.recurrence == 'monthly':
                # Calcula o próximo mês e mantém o mesmo dia
                month_increment = (current_date.month % 12) + 1
                year_increment = current_date.year + (current_date.month // 12)
                try:
                    current_date = current_date.replace(year=year_increment, month=month_increment)
                except ValueError:
                    # Se o dia não existir no próximo mês, pule para o próximo mês válido
                    while True:
                        month_increment = (month_increment % 12) + 1
                        year_increment += (month_increment // 12)
                        try:
                            current_date = current_date.replace(year=year_increment, month=month_increment)
                            break
                        except ValueError:
                            continue
            elif event.recurrence == 'yearly':
                current_date = current_date.replace(year=current_date.year + 1)

            occurrences += 1

        event_df = pd.DataFrame(event_list)
        self.df = pd.concat([self.df, event_df], ignore_index=True)
        self.db_manager.save_data(self.df)

    def remove_event_by_name(self, name):
        """
        Remove todas as ocorrências de um evento.
        """
        self.df = self.df[self.df['name'] != name].reset_index(drop=True)
        self.db_manager.save_data(self.df)

    def remove_event_by_name_and_date(self, name, date):
        """
        Remove um evento apenas em uma data específica.
        """
        date = datetime.strptime(date, '%d/%m/%Y')
        self.df = self.df[(self.df['name'] != name) | (self.df['date'] != date)].reset_index(drop=True)
        self.db_manager.save_data(self.df)

    def remove_all_events(self):
        """
        Remove todos os eventos do calendário.
        """
        # Recria o DataFrame sem nenhuma linha, mantendo as mesmas colunas
        self.df = pd.DataFrame(columns=self.df.columns)
        # Salva o DataFrame vazio usando o DatabaseManager
        self.db_manager.save_data(self.df)

    def list_all_events(self):
        """
        Lista os eventos.
        """
        if self.df.empty:
            print("Nenhum evento cadastrado.")
        else:    
            return self.df.sort_values(by='date')
    
    def list_events_today(self):
        """
        Lista todos os eventos de hoje.
        """
        today = datetime.now().date()
        events = self.df[self.df['date'].dt.date == today]

        if events.empty:
            print("Nenhum evento para hoje")
        else:
            return events.sort_values(by='start_time')

    def list_events_date(self, date):
        """
        Lista todos os eventos de uma data específica.
        """
        specific_date = datetime.strptime(date, '%d/%m/%Y').date()
        events = self.df[self.df['date'].dt.date == specific_date]

        if events.empty:
            print("Nenhum evento para a data.")
        else:
            return events.sort_values(by='start_time')

    def list_events_until_date(self, date):
        """
        Lista todos os eventos que acontecem entre hoje e uma data específica.
        """
        today = datetime.now().date()
        end_date = datetime.strptime(date, '%d/%m/%Y').date()
        events = self.df[(self.df['date'].dt.date >= today) & (self.df['date'].dt.date <= end_date)]

        if events.empty:
            print("Nenhum evento para o período")
        else:
            return events.sort_values(by=['date', 'start_time'])
    
    def list_events_interval(self, start_date, end_date):
        """
        Lista todos os eventos que acontecem em dado intervalo de tempo.
        """
        start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
        end_date = datetime.strptime(end_date, '%d/%m/%Y').date()
        events = self.df[(self.df['date'].dt.date >= start_date) & (self.df['date'].dt.date <= end_date)]

        if events.empty:
            print("Nenhum evento para o período")
        else:
            return events.sort_values(by=['date', 'start_time'])

    def find_events_by_name(self, search_term):
        """
        Encontra eventos de acordo com um termo de pesquisa.
        """
        events = self.df[self.df['name'].str.contains(search_term, na=False, case=False)]

        if events.empty:
            print("Nenhum evento com este nome")
        else:
            return events.sort_values(by=['date', 'start_time'])

    def list_events_category(self, category):
        """
        Lista todos os eventos de uma categoria específica.
        """
        events = self.df[self.df['category'] == category]

        if events.empty:
            print("Nenhum evento para a categoria.")
        else:
            return events.sort_values(by=['date', 'start_time'])
    
    def list_categories(self):
        """
        Lista todas as categorias únicas de eventos existentes no calendário.
        """
        return list(self.df['category'].dropna().unique())
    
    def edit_events_by_name(self, event_name, changes):
        """
        Edita todos os eventos que têm o mesmo nome no calendário.
        """
        event_indices = self.df[self.df['name'].str.lower() == event_name.lower()].index
        for index in event_indices:
            for key, value in changes.items():
                if key in self.df.columns:
                    self.df.at[index, key] = value
        self.db_manager.save_data(self.df)

    def edit_event(self, name, event_date, changes):
        """
        Edita um evento específico no calendário baseado no nome e na data do evento.
        """
        # Converte a string da data para um objeto datetime.date
        # event_date = datetime.strptime(event_date, '%d/%m/%Y').date()
        
        # Filtra o DataFrame para encontrar o evento específico
        event_indices = self.df[(self.df['name'].str.lower() == name.lower()) & (self.df['date'] == event_date)].index
        
        # Caso não encontre nenhum evento, retorna uma mensagem de erro
        if event_indices.empty:
            print("Nenhum evento encontrado com esse nome e data.")
            return
        
        # Aplica as mudanças ao primeiro evento encontrado
        for index in event_indices:
            for key, value in changes.items():
                if key in self.df.columns:
                    self.df.at[index, key] = value
    
        # Salva as mudanças no arquivo
        self.db_manager.save_data(self.df)