from view.output_manager import OutputManager
from database.database_manager import DatabaseManager
from models.calendar import Calendar
from models.event import Event

from datetime import datetime

def handle_input():
    db_manager = DatabaseManager('eventos.pkl')
    calendar = Calendar(db_manager)

    while True:
        OutputManager.main_menu()
        action = int(input())

        """
        Adicionar evento
        """
        if action == 1:

            OutputManager.adding_event()
            nome = input("Nome do evento: ")
            date = input("Data do evento (DD/MM/YYY): ")
            start_time = input("Hora de início (HH:MM, opcional): ")
            end_time = None
            if start_time:  # Se uma hora inicial for fornecida, pergunta a hora de término
                end_time = input("Hora de término (HH:MM, opcional): ")
            category = input("Categoria (opcional): ")

            OutputManager.choose_recurrence_menu()
            recurrence = int(input())

            # Evento unico
            if recurrence == 1:
                recurrence = None
                event = Event(nome, date, start_time if start_time else None, end_time if end_time else None, category, recurrence)
                calendar.add_event(event)

            # Evento recorrente
            else:
                if recurrence == 2:
                    recurrence = 'daily'
                elif recurrence == 3:
                    recurrence = 'weekly'
                elif recurrence == 4:
                    recurrence = 'monthly'
                elif recurrence == 5:
                    recurrence = 'yearly'

                event = Event(nome, date, start_time if start_time else None, end_time if end_time else None, category if category else None, recurrence)
                
                OutputManager.choose_recurrence_limit_menu()

                limit = int(input())
                if limit == 1:
                    end_date = input("Data limite: ")
                    calendar.add_recurrent_event_by_end_date(event, end_date)
                if limit == 2:
                    num_occurrences = input("Número de ocorrências: ")
                    calendar.add_recurrent_event_by_num_occurrences(event, int(num_occurrences))

        """
        Remover evento
        """
        if action == 2:
            
            OutputManager.remove_event_menu()
            opt = int(input())

            if opt == 1:
                OutputManager.removing_event()
                name = input("Digite o nome do evento: ")
                events = calendar.find_events_by_name(name)
                if len(events) > 1:
                    print("Foram encontrados os seguintes eventos:")
                    print("=======================")
                    print(events)
                    OutputManager.choose_removing_type()
                    opt = int(input())
                    if opt == 1:
                        calendar.remove_event_by_name(name)
                    if opt == 2:
                        date = input("Data: ")
                        calendar.remove_event_by_name_and_date(name, date)
                else:
                    calendar.remove_event_by_name(name)

            elif opt == 2:
                data = input("Digite a data: ")
                # todo

            elif opt == 3:
                sure = input("Tem certeza que quer apagar TODOS os eventos? [Y/n]: ")
                if sure == "Y":
                    calendar.remove_all_events()

        """
        Editar evento
        """
        if action == 3:

            OutputManager.editing_event()
            name = input("Digite o nome do evento que deseja editar: ")
            events = calendar.find_events_by_name(name)
            if len(events) > 0:
                print("Foram encontrados os seguintes eventos:")
                print("=======================")
                print(events)
                OutputManager.choose_editing_type()
                choice = int(input("Escolha uma opção: "))
                
                if choice == 1:
                    event_date = input("Digite a data do evento que deseja editar (DD/MM/YYY): ")
                    matching_events = events[events['date'] == datetime.strptime(event_date, '%d/%m/%Y')]
                    if len(matching_events) > 1:
                        print("Mais de um evento encontrado nessa data. Por favor, informe o horário de início do evento que deseja editar (HH:MM):")
                        event_start_time = input("Horário de início: ")
                        matching_event = matching_events[matching_events['start_time'] == event_start_time]
                        event_index = matching_event.index[0]
                    else:
                        event_index = matching_events.index[0]
                    
                    print("Digite as novas informações para o evento. Deixe em branco para não alterar.")
                    date = input("Nova data (DD/MM/YYY): ")
                    start_time = input("Novo horário de início (HH:MM): ")
                    end_time = input("Novo horário de término (HH:MM): ")
                    category = input("Nova categoria: ")
                    
                    changes = {}
                    if date: changes['date'] = datetime.strptime(date, '%Y-%m-%d')
                    if start_time: changes['start_time'] = start_time
                    if end_time: changes['end_time'] = end_time
                    if category: changes['category'] = category
                    
                    calendar.edit_event(name, event_date, changes)
                    print("Evento atualizado com sucesso!")
                    input("enter")
                
                elif choice == 2:
                    print("Digite as novas informações para os eventos. Deixe em branco para não alterar.")
                    date = input("Nova data (DD/MM/YYY): ")
                    start_time = input("Novo horário de início (HH:MM): ")
                    end_time = input("Novo horário de término (HH:MM): ")
                    category = input("Nova categoria: ")
                    
                    changes = {}
                    if date: changes['date'] = datetime.strptime(date, '%Y-%m-%d')
                    if start_time: changes['start_time'] = start_time
                    if end_time: changes['end_time'] = end_time
                    if category: changes['category'] = category
                    
                    calendar.edit_events_by_name(name, changes)
                    print("Todos os eventos atualizados com sucesso!")
            else:
                print("Nenhum evento encontrado com esse nome.")


        """
        Listar eventos
        """
        if action == 4:
        
            OutputManager.list_events_menu()
            opt = int(input())
            if opt == 1:
                events = calendar.list_all_events()
                if events is not None: 
                    print(events)
            
            elif opt == 2:
                events = calendar.list_events_today()
                if events is not None:
                    print(events)

            elif opt == 3:
                data = input("Data: ")
                events = calendar.list_events_date(data)
                if events is not None:
                    print(events)

            elif opt == 4:
                data = input("Data: ")
                events = calendar.list_events_until_date(data)
                if events is not None:
                    print(events)

            elif opt == 5:
                start = input("Data de início: ")
                end = input("Data de término: ")
                events = calendar.list_events_interval(start, end)
                if events is not None:
                    print(events)

            elif opt == 6:
                term = input("Nome do evento: ")
                events = calendar.find_events_by_name(term)
                if events is not None:
                    print(events)

            elif opt == 7:
                cat = input("Categoria: ")
                events = calendar.list_events_category(cat)
                if events is not None:
                    print(events)

            elif opt == 8:
                print(calendar.list_categories())
            
            input("\nPressione Enter para voltar ao menu")


        """
        Sair
        """
        if action == 5:
            break