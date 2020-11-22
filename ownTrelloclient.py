# Собственный клиент для Trello API
import sys
import requests

auth_params = {
    'key': 'd85df1f9b2cf5270e14c26546bb86e08',
    'token': 'f4d461a88735a8125321e99a7d09e8969fb3ce4173a09d63842f5a80931356c1'
}
#Адрес, куда будут отпраляться запросы
base_url = 'https://trello.com/1/{}'
board_id = 'Ujj8LhLp'

def read():
    #Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    #Выведем название каждой колоноки и всех заданий, которые к ней относятся :
    for column in column_data:
        print(column['name'])
        #Получим названи всех задач в колонке и перечислим все назвния
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])

#Функция, позволяющая создать задачу с произвольным названием в одной из колонок
def create(name, column_name):
    #Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_data:
        if column['name'] == column_name:
            #Создадим задачу с именем __name__ в найденной колонке
            requests.post(base_url.format('cards'), data={'name':name, 'idList':column['id'], **auth_params})

#Функция перемещения задач между колонками
def move(name, column_name):
    #Получаем данные всех колонок на доске
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    #Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
            if task_id:
                break
    #Теперь, когда есть id задачи, которыую хотели перенести
    #перебераем данные обо всех колонках , пока не найдём ту, в которую будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            # и выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break




#create('Изучить Python', 'Нужно сделать')
# Если передано два или меньше параметра, скрипт будет выполнять фунцию read().
# Иначе будет выполняться функция , которая ожидает передачи ещё двух параметров —
# названия создаваемой задачи и названия колонки, в которой эта задача будет создаваться.
if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])