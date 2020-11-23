# Собственный клиент для Trello API
import sys
import requests

auth_params = {
    'key': '', #введите совой ключ разработчика 
    'token': '' #введите свой токен
}

base_url = 'https://trello.com/1/{}'
board_id = '' #введите id доски

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

#Чтение всех колонок и задач
def read():      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    counter_tasks = counterTasks()
    for column in column_data:      
        print(str(counter_tasks[column['id']])+' '+ column['name'])    
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'] + " id задачи: " + task['id'])    

#Создание задачи
def createCard(name, column_name):      
    column_id = column_check(column_name)
    if column_id is None:
        column_id = createColumn(column_name)['id']
    requests.post(base_url.format('cards'), data={'name': name, 'idList': column_id, **auth_params})

#Создание колонки
def createColumn(column_name):            
    return requests.post(base_url.format('lists'), data={'name': column_name, 'idBoard': board_id, **auth_params}).json() 

#Премещение задачи
def move(name, column_name): 
    dublicate_tasks = getDublicate(name)   
    if len(dublicate_tasks) > 1:  
        print("Задач с таким названием несколько:")  
        for task in dublicate_tasks:  
            task_column_name = requests.get(base_url.format('lists') + '/' + task['idList'], params=auth_params).json()['name']  
            print("задача с id: {}\tНаходится в колонке: {}\t ".format(task['id'], task_column_name))  
        task_id = input("Пожалуйста, введите ID задачи, которую нужно переместить: ")  
    else:  
        task_id = duplicate_tasks[0]['id']        
    column_id = column_check(column_name)
    if column_id is None:
        column_id = create_column(column_name)['id']    
    requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column_id, **auth_params})
  

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'createCard':
        createCard(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
         move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'createColumn':
        createColumn(sys.argv[2])

