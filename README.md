# Trabalho de Teste de Software

## Membros
- **João Luiz Lopes Megale** - 2020006671

## Sistema
Foi desenvolvido um sistema de agenda que permite ao usuário gerenciar eventos por meio da linha de comando. Nesta agenda, é possível adicionar, remover, editar e buscar por eventos.

### Funcionalidades

#### Adicionar Evento
O usuário pode adicionar eventos que ocorram uma única vez, bem como eventos recorrentes (diários, semanais, mensais e anuais).

#### Remover Evento
O usuário pode remover eventos buscando pelo nome. Quando há diversos eventos com o mesmo nome, é possível remover todos os eventos ou apenas um específico. Também é possível remover todos os eventos cadastrados até então.

#### Editar Evento
O usuário pode editar as características (nome, data, horário e categoria) de um ou mais eventos.

#### Listar Eventos
O usuário pode listar os eventos disponíveis de diversas formas, utilizando diferentes critérios, como por exemplo: eventos do dia de hoje, eventos com data/nome/categoria específica, eventos em um intervalo de tempo específico, etc.

## Tecnologias Utilizadas
- A linguagem de programação usada foi Python.
- O framework de teste utilizado foi o unittest.
- A interface com o usuário é inteiramente via linha de comando.
- Para manipulação dos dados, foi utilizada a biblioteca Pandas, e para o armazenamento, foi utilizado um arquivo pickle .pkl, que é criado no diretório do usuário ao rodar o programa pela primeira vez.
