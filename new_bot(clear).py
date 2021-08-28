import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import os
import bot_modul3(clear) as bot
import time
import vk
import pandas as pd
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id

#Шаблонный код для подключения к группе ВК.
vk_session = vk_api.VkApi(token='Ваш токен vk api')
longpoll = VkLongPoll(vk_session)
vk_api =vk_session.get_api()

cat = "Ваш токен vk api"
session = vk.Session(access_token=cat)
vk_api_1 = vk.API(session)
upload = VkUpload(vk_api)

#метод create_base() - создает базу данных в csv формате с которой можно работать.

# метод pick(event, names_pick = [],text = "str" , item = "str" , callback = [] , savepoint_add = [колонка, значение], savepoint_check = "str") - Создание диалогового окна взаимодействия с пользователем. 

#names_pick- создание кнопок на которые может нажать пользователей, названия кнопок являются триггером для запуска цепочки callback
#text - тест сообщения с кнопками
#item - ссылка на медиа файл существующий в вк для прикрепления его к сообщению.
#callback -реакция на определенные строковые сообщения, может записываться в массиве.
#savepoint_add - запись состояния перехода по кнопке у указанную колонку по id пользователя. (Обязательно использование callback)
#savepoint_check - условие перехода в блок. Если текущие состояние пользователя (Обязательно использование callback и savepoint_add для изменения состояния) .

#Шаблонный код для подключения к группе ВК.

bot.create_base()
base_quest  = bot.take_quests()
print(base_quest)
d = "\\"
d = "/"

def quest_ask(event, base_quest):
	quest_serias = bot.taker_value(event, "random_quest")
	quest_serias  = quest_serias.split(',')
	order = bot.taker_value(event, "order_num")
	order = int(order)
	q = int(quest_serias[order])
	bot.send_photo(vk_api, event.user_id, *bot.upload_photo(upload, base_quest[q][3]))
	bot.door(event = event, names_pick = base_quest[q][2], text ="Какой градации параметр: <" + base_quest[q][0] + "> ?")
	bot.sheet_add(event, "true_answer", base_quest[q][1])
	text = ""
	for i in base_quest[q][2]:
		text = text  + i + ","
	bot.sheet_add(event, "all_answers", text)


def answer_check(event):
	if event.text == str(bot.taker_value(event, "true_answer")):
		vk_api.messages.send(user_id= event.user_id, message= "Ответ правильный" , random_id = random.randint(1, 10000000))
	else:
		vk_api.messages.send(user_id= event.user_id, message= "Ответ НЕ правильный" , random_id = random.randint(1, 10000000))
		vk_api.messages.send(user_id= event.user_id, message= "Правильный ответ : " + str(bot.taker_value(event, "true_answer")) , random_id = random.randint(1, 10000000))
		error = bot.taker_value(event, "count_error")
		error = error + 1
		bot.sheet_add(event, "count_error", error)

	bot.sheet_add(event, "true_answer", "NON")
	bot.sheet_add(event, "all_answers", "NON")
	order = int(bot.taker_value(event, "order_num"))
	order = order + 1
	bot.sheet_add(event, "order_num", order)
	bot.sheet_add(event, "check_point", "Another_an")
	if order > 8:
		bot.door(event = event, names_pick = ["Меню"], text = "Игра окончена, колличество допущенных ошибок: "  + str(bot.taker_value(event, "count_error")))
		bot.sheet_add(event, "check_point", "menu")

def gen_quest(event, base_quest):
	if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me and event.text in ["Начать игру"] and "Game_sort" == bot.save_point(event):
		quest_num = random.sample(range(1,len(base_quest) - 1), int(len(base_quest) - 2))
		text = ""
		print(quest_num)
		for r in quest_num:
			text = text  + "," + str(r)
		bot.sheet_add(event, column_name = "random_quest", text = text)
		bot.door(event = event, text = "Индивидуальный список вопросов формируется. Пожалуйста, подождите...", savepoint_add = ['check_point', "answerON"], savepoint_check = "Game_sort")
		bot.sheet_add(event, column_name = "order_num", text = 1)
		bot.sheet_add(event, "count_error", 0)
		quest_ask(event, base_quest)

def arcade_game(event, base_quest):
	bot.door(event = event, names_pick = ["Начать игру", "Меню"], text = "Данная игра генерирует случайный неповторяющийся список вопросов.", callback = ["Аркада"], savepoint_add = ['check_point', "Game_sort"], savepoint_check = "startgame")
	gen_quest(event, base_quest)
	try:
		if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me and event.text in bot.taker_value(event, "all_answers") and bot.save_point(event) in ["answerON"]:
			answer_check(event)
	except:
		print("Новый игрок")
		vk_api.messages.send(user_id= event.user_id, message= "Приветствуем нового игрока" , random_id = random.randint(1, 10000000))
		bot.sheet_add(event, "true_answer", "NON")
		bot.sheet_add(event, "all_answers", "NON")

	if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me and event.text in bot.taker_value(event, "all_answers") and bot.save_point(event) in ["Another_an"]:
		answer_check(event)
	if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me and event.text and "Another_an" in bot.save_point(event):
		quest_ask(event, base_quest)


def cat_run():
	for event in longpoll.listen():
		bot.user_add(event)
		if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me:	
			bot.key(event)
			text_base_of_knows = "Список для базы знаний (FAQ) \n Как проходить обучение: \n ссылка \n\n Влияние пластических операций: \n ссылка \n\n Средние черты и промежуточные показатели: \n ссылка \n\n Общие рекомендации о том каак начать делать описания: \n ссылка \n\nС какого возраста можно делать описания?: \n ссылка"
			bot.door(event = event, names_pick = ["Игры", "База знаний"], text = "Открыто главное меню", callback = ["/start", "Начать", "Меню"], item = "doc254413230_554019683", savepoint_add = ['check_point', "menu"])
			bot.door(event = event, names_pick = ["FAQ и статьи", "3д модели", "Примеры черт" ], text = "Открыт раздел базы знаний", callback = ["База знаний"], item = "doc254413230_519934722")
			bot.door(event = event, names_pick = ["Меню", "3д модели", "Примеры черт" ], text = text_base_of_knows, callback = ["FAQ и статьи"], item = "")
			bot.door(event = event, names_pick = ["FAQ и статьи", "Меню", "Примеры черт" ], text = "ссылка", callback = ["3д модели"])
			bot.door(event = event, names_pick = ["FAQ и статьи", "3д модели", "Меню" ], text = "ссылка", callback = ["Примеры черт"])
			bot.door(event = event, names_pick = ["Аркада", "Меню"], text = "Игровой кабинет", callback = ["Игры"], savepoint_add = ['check_point', "startgame"])

			arcade_game(event, base_quest = base_quest)

def g_forse():
	try:
		cat_run()
	
	except Exception as e:
		print(e)

		print("бот вырубился")

		
		time.sleep(3)	
		g_forse()
#cat_run()
g_forse()

