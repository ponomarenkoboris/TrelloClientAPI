#Работа с Trello API
from trello import TrelloApi

api_key = 'd85df1f9b2cf5270e14c26546bb86e08'#Ключ разработчика
token = 'f4d461a88735a8125321e99a7d09e8969fb3ce4173a09d63842f5a80931356c1'#Персональный токен
trello = TrelloApi(api_key, token)

response = trello.boards.new('Created with API')#Отпрваляем запрос на создание новой доски
print(response)
board_id = response['id']#Берём параметр id
for column in trello.boards.get_list(board_id): #Выводим все колонки с доски
	print(column['name'])

for column in trello.boards.get_list(board_id):
	if 'Нужно' in column['name']:
		list_id = column['id']
		print(trello.lists.get_card(list_id))

card = trello.cards.new('Научиться использовать Trello API', list_id)#Создаём запись в указанной колонке
print(card)