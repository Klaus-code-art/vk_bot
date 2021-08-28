import vk_api
import random
import os
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkApi as vk
import pandas as pd #Для работы с талицами
from datetime import datetime, date, time
import time
import pandas as pd
import vk as vkbot


#Шаблонный код для подключения к группе ВК.
vk_session = vk_api.VkApi(token='vk api')
longpoll = VkLongPoll(vk_session)
vk =vk_session.get_api()

cat = "vk api"
session = vkbot.Session(access_token=cat)
vk_api_1 = vkbot.API(session)

def create_base():
	path = str(os.getcwd())
	if 'playes_base.csv' in os.listdir(path):
		fixed_df = pd.read_csv('playes_base.csv')# Путь, куда вы скачали файл
	else:
		df =  data = {
		"vk_id": [],
		"nickname": [],
		"check_point": [],
		"door" : []
		} # Этот столбец отвечет за указание порядкового номера вопроса на котором остановился юзер
		frame = pd.DataFrame(data)
		frame.to_csv('playes_base.csv', index=False)
		print("Создаю файл логирования данных действий игроков не найден")
		print("Создаю файл логирования данных действий игроков")

d = "\\"
d = "/"



def key(event):
	chat_id_users = vk_api_1.messages.getConversationMembers(peer_id= 2000000005 ,  v=5.126 )
	id_users = []
	for i in chat_id_users["profiles"]:

		id_users.append(i["id"])
		id_users.append(i["last_name"])
	if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me and lock_point(event) != "unlock":
		print(id_users)
		if event.user_id in id_users:
			sheet_add(event, column_name = "door", text = "unlock")
			vk.messages.send(user_id= event.user_id, message= "Доступ открыт" , random_id = random.randint(1, 10000000))


def test_lock(event):
	if event.type == VkEventType.MESSAGE_NEW and event.text in ["lock", "Lock"] and event.to_me:
			vk_api.messages.send(user_id= event.user_id, message= "Ключ активен" , random_id = random.randint(1, 10000000))
			bot.sheet_add(event, column_name = "door", text = "lock")

def user_add(event):
	if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me:
		df = pd.read_csv(str(os.getcwd()) + d +'playes_base.csv')
		check_id = str(df[df["vk_id"] == event.user_id]["vk_id"])
		df = pd.read_csv(str(os.getcwd()) + d +'playes_base.csv')

		if str(event.user_id) in check_id:
			a = 0
		else:
			df = df.append({"vk_id": str(event.user_id)}, ignore_index=True)
			df.to_csv('playes_base.csv', encoding = 'utf-8', index=False)
			user_add(event)


def sheet_add(event, column_name = "", text = 0):
	df = pd.read_csv(str(os.getcwd()) + d +'playes_base.csv')
	df.loc[df.vk_id == event.user_id, column_name] = str(text)
	df.to_csv('playes_base.csv', encoding = 'utf-8', index=False)
	print(df)


def save_point(event):
	df = pd.read_csv(str(os.getcwd()) + d +'playes_base.csv')
	check_id_list = df[df["vk_id"] == event.user_id]["check_point"]
	for i in check_id_list:
		a = 0
	return str(i)

def lock_point(event):
	df = pd.read_csv(str(os.getcwd()) + d +'playes_base.csv')
	check_id_list = df[df["vk_id"] == event.user_id]["door"]
	for i in check_id_list:
		z = 0
	return str(i)

def user_authtification(event):
	chat_id_users = vk_api.messages.getConversationMembers(peer_id= 2000000001 ,  v=5.126 )

	id_users = []


	for i in chat_id_users["profiles"]:

		id_users.append(i["id"])
	print(id_users)
	return id_users


def user_denied(event, call = "Начать"):
	id = user_authtification(event)
	if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me and (event.text in call) and "unlock" != save_point(event):
		if event.user_id in id:
			vk_api.messages.send(user_id= event.user_id, message= "Вы состоите в чате, проверка пройдена" , random_id = random.randint(1, 10000000))
			sheet_add(event, column_name = "check_point", text = "unlock")
		else:
			vk_api.messages.send(user_id= event.user_id, message= "Вас нет в списке игроков, пожалуйста обратитесь к куратору" , random_id = random.randint(1, 10000000))



def vk_print(event,names_pick = 0 ,text = "ми", item = "", keyboard = "keyboard"):
	try:
		vk.messages.send(user_id= event.user_id, message= text , random_id = random.randint(1, 10000000), keyboard=keyboard.get_keyboard(), attachment = item)
	except:
		vk.messages.send(user_id= event.user_id, message= text , random_id = random.randint(1, 10000000), attachment = item)

def pick(event, names_pick = [],text = "ми", item = "" , callback = 0 , savepoint_add = [], savepoint_check = 0):
	user_add(event = event)
	
	if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me:
		
		keyboard = VkKeyboard(one_time=True)


		if len(names_pick) > 2:
			count  = len(names_pick) - 1
			for i in names_pick:
				keyboard.add_button(i, color=VkKeyboardColor.POSITIVE)
				if count != 0:
					keyboard.add_line()
					count = count - 1
		else:
			for i in names_pick:
				keyboard.add_button(i, color=VkKeyboardColor.POSITIVE)
				

		if (callback == 0)  and (savepoint_check == 0): #Еслии ничего не написаноы
			vk_print(event, keyboard = keyboard, text = text, item = item) 
			print("1")

		if savepoint_add != 0 and callback != 0 and (savepoint_check == 0):
			if event.type == VkEventType.MESSAGE_NEW and event.text  and event.to_me and (event.text in callback):
				sheet_add(event, savepoint_add[0], savepoint_add[1] )
				vk_print(event, keyboard = keyboard, text = text, item = item)
				print("2")

		if (callback != 0) and (savepoint_check != 0) and (savepoint_add != 0):
			if event.type == VkEventType.MESSAGE_NEW and (event.text in callback) and event.to_me and savepoint_check == save_point(event):
				vk_print(event, keyboard = keyboard, text = text, item = item)
				sheet_add(event, savepoint_add[0], savepoint_add[1] )
				print("3")

		if (callback != 0) and (savepoint_check != 0) and (savepoint_add == 0):
			if event.type == VkEventType.MESSAGE_NEW and (event.text in callback) and event.to_me and savepoint_check == save_point(event):
				vk_print(event, keyboard = keyboard, text = text, item = item)
				print("4")
		
		if (callback != 0) and (savepoint_check == 0) and (savepoint_add == 0):
			if event.type == VkEventType.MESSAGE_NEW and (event.text in callback) and event.to_me:
				vk_print(event, keyboard = keyboard, text = text, item = item)
				print("5")

		if (callback == 0) and (savepoint_check != 0) and (savepoint_add == 0):
			if event.type == VkEventType.MESSAGE_NEW and (event.text in callback) and event.to_me and savepoint_check == save_point(event):
				vk_print(event, keyboard = keyboard, text = text, item = item)
				print("6")
		
		if (callback == 0) and (savepoint_check != 0) and (savepoint_add != 0):
			if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me and savepoint_check == save_point(event):
				vk_print(event, keyboard = keyboard, text = text, item = item)
			
				sheet_add(event, savepoint_add[0], savepoint_add[1])
				print("7")

def door(event, names_pick = [],text = "ми", item = "" , callback = 0 , savepoint_add = 0, savepoint_check = 0):
	if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me and "unlock" == str(lock_point(event)):
		pick(event, names_pick, text, item, callback, savepoint_add, savepoint_check)


def take_quests(test = "Тесты_НТ", base_quest = {}):

	first_path = str(os.getcwd())
	os.chdir(first_path  + d + test)
	a = 0

	for i in os.listdir(os.getcwd()):
		run_1 = str(os.getcwd())  + d + i
		back_1 = str(os.getcwd())
		os.chdir(run_1)

		for j in os.listdir(os.getcwd()):
			
			run_2 = str(os.getcwd())  + d + j
			back_2 = str(os.getcwd())
			os.chdir(run_2)

			for k in os.listdir(os.getcwd()):
				t_mass = []
				a = a + 1
				h =  os.getcwd()
				os.chdir(back_2)

				for t in os.listdir(os.getcwd()):
					t_mass = t_mass + [t]
				os.chdir(run_2)
				path_text = h + d + k
				print(a)
				base_quest.setdefault(a, [i, j, t_mass, path_text])
			os.chdir(back_2)
		os.chdir(back_1)
	print(base_quest)
	os.chdir(first_path)

	return base_quest

def upload_photo(upload, photo):
	response = upload.photo_messages(photo)[0]

	owner_id = response['owner_id']
	photo_id = response['id']
	access_key = response['access_key']

	return owner_id, photo_id, access_key


def send_photo(vk, peer_id, owner_id, photo_id, access_key):
	attachment = f'photo{owner_id}_{photo_id}_{access_key}'
	vk.messages.send(
		random_id=get_random_id(),
		peer_id= peer_id,
		attachment=attachment)

def taker_value(event, colomn):
	df = pd.read_csv(str(os.getcwd()) + d +'playes_base.csv')
	check_id_list = df[df["vk_id"] == event.user_id][colomn]
	for i in check_id_list:
		count_quests = i
#		print(count_quests)
#		print(type(count_quests))
	return i
