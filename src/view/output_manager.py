import os

class OutputManager:

    def main_menu():
        OutputManager._clear()
        print("=======================")
        print("Bem vindo à sua agenda\n")
        print("Escolha alguma das ações abaixo:")
        print('1 - Adicionar evento')
        print('2 - Remover evento')
        print('3 - Editar evento')
        print('4 - Listar eventos')
        print('5 - Sair')
        print("=======================")
        print("Resposta: ", end='')

    def adding_event():
        OutputManager._clear()
        print("====| Adicionando Evento |====")

    def choose_recurrence_menu():
        OutputManager._clear()
        print("Qual a recorrência do projeto?")
        print("=======================")
        print("1 - Único")
        print("2 - Diário")
        print("3 - Semanal")
        print("4 - Mensal")
        print("5 - Anual")
        print("=======================")
        print("Resposta: ", end='')

    def choose_recurrence_limit_menu():
        OutputManager._clear()
        print("Até quando o evento será recorrente?")
        print("=======================")
        print("1 - Até uma data limite")
        print("2 - Até certo número de ocorrências")
        print("=======================")
        print("Resposta: ", end='')

    def remove_event_menu():
        OutputManager._clear()
        print("Remover um Evento")
        print("=======================")
        print("1 - Remover evento por nome")
        print("2 - Remover evento por data")
        print("3 - Remover todos os eventos")
        print("=======================")
        print("Resposta: ", end='')

    def removing_event():
        OutputManager._clear()
        print("====| Removendo Evento |====")

    def choose_removing_type():
        print("=======================")
        print("1 - Remover todos os eventos com este nome")
        print("2 - Especificar data do evento a ser removido")
        print("=======================")
        print("Resposta: ", end='')

    def editing_event():
        OutputManager._clear()
        print("====| Editando Evento |====")

    def choose_editing_type():
        print("=======================")
        print("1 - Especificar data do evento a ser editado")
        print("2 - Editar todos os eventos com este nome")
        print("=======================")
        print("Resposta: ", end='')

    def list_events_menu():
        OutputManager._clear()
        print("Quais eventos deseja listar?")
        print("=======================")
        print("1 - Listar todos os eventos")
        print("2 - Listar os eventos de hoje")
        print("3 - Listar os eventos de uma data específica")
        print("4 - Listar os eventos de hoje até uma data específica")
        print("5 - Listar os eventos dentro de um intervalo de tempo")
        print("6 - Buscar eventos pelo nome")
        print("7 - Listar os eventos de uma categoria")
        print("8 - Listar todas as categorias existentes")
        print("=======================")
        print("Resposta: ", end='')

    def _clear():
        os.system('cls' if os.name == 'nt' else 'clear')