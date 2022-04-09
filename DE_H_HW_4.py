import sqlite3 # pip install db-sqlite3
import json
connect = sqlite3.connect('client.db')
cursor = connect.cursor()
#############################################################################

# 1) Функция, которая создает таблицу client, если она уже есть, 
# необходимо вывести об этом сообщение в консоль
def init_table():
	try:
		cursor.execute('''
			CREATE TABLE client(
				id integer primary key autoincrement,
				name varchar(128),
				lastname varchar(128),
				age integer
			)
		''')
	except sqlite3.OperationalError:
		print('Таблица client уже создана')
		
init_table()

#############################################################################

# 2) Функция, которая добавляет клиентов в таблицу 
# (если клиента с такими фамилией и именем нет в таблице)
def addClient(name, lastname, age):
	cursor.execute('select count(*) from client where name = ? and lastname = ?', [name, lastname])
	
	if cursor.fetchone()[0] != 0:
		print(f'Клиент {name} {lastname} уже есть в базе')
		
	else:
		cursor.execute('''
			INSERT INTO client (name, lastname, age)
			VALUES (?, ?, ?)''', [name, lastname, age])

	connect.commit()

addClient('Бродяга', 'Ширешагин', 65)
addClient('Федя', 'Сумкин', 35)
addClient('Пин', 'Пипин', 36)
addClient('Гена', 'Серый', 93)
addClient('Сарик', 'Белый', 101)

#############################################################################

# 3) Функция, которая получив путь до JSON файла и добавляет клиентов в таблицу
# (только тех, которые по фамилии и имени отсутствуют в таблице)
def loadFromJSON(path):
	with open(path, 'r', encoding = 'utf-8') as f:
		clients = json.load(f)
		for client in clients:
			addClient(**client)

	connect.commit()

loadFromJSON('task_data.json')

#############################################################################

# 4) Функция, которая возвращает средний возраст клиентов.
def avgAge():
	cursor.execute('SELECT avg(age) FROM client')
	for row in cursor.fetchall()[0]:
		print('Средний возраст клиентов ', int(row))
avgAge()

#############################################################################



# Вывод таблицы для просмотра 
def printTable(tableName):
	print('*~'*12)
	print('~*'+' '*4+tableName+' '*4+'*~')
	print('*~'*12)
	cursor.execute(f'select * from {tableName}')
	for row in cursor.fetchall():
		print(row)
	print('~*'*12+'\n')  

printTable('client')
