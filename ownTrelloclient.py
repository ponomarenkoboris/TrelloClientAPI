# Собственный клиент для Trello API
import sys
import requests

auth_params = {
    'key': 'd85df1f9b2cf5270e14c26546bb86e08',
    'token': 'f4d461a88735a8125321e99a7d09e8969fb3ce4173a09d63842f5a80931356c1'
}

base_url = 'https://trello.com/1/{}'
board_id = 'Bwnvs8UF'

def column_check(column_name):
    column_id = None
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            column_id = column['id']
            return column_id
        
def getDublicate(task_name):

    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    dublicate_tasks = []
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in task_data:
            if task_name == task['name']:
                dublicate_tasks.append(task)
    return dublicate_tasks

def counterTasks():
    counter_tasks = {}
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        counter_tasks[column['id']] = len(task_data)
    return counter_tasks

#Создание новой колонки
def createColumn(new_colomn_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == new_colomn_name:
            print('Колонка с ткаим именем уже существует')
            return
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': new_colomn_name, **auth_params})

#Чтение данных всех колонки
def read():
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        counter = len(task_data)
        print(column['name'], f'(количество задач: {counter})')
        if not task_data:
            print('\t' + 'Нет задач!')
            continue
        for task in task_data:
            print('\t' + task['name'])


#Создание карточки
def createCard(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == column_name:
            print(column)
            requests.post(base_url.format('cards'), data={'name':name, 'idList':column['id'], **auth_params})



#Премещение карточки
def move(name, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                task_id = task['id']
                break
            if task_id:
                break

    for column in column_data:
        if column['name'] == column_name:
            # и выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            break


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'createCard':
        createCard(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
         move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'createColumn':
        createColumn(sys.argv[2])

