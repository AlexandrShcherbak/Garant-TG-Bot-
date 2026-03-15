# -*- coding: utf-8 -*-
from decimal import *
import datetime
import json
import os
import random
import shutil
import sqlite3
import subprocess
import time

import telebot
from telebot import apihelper, types

import config
# from Light_Qiwi import Qiwi, OperationType
import keyboards
import requests
from datetime import datetime, timedelta
# BOT

bot = telebot.TeleBot(config.bot_token)
global users_id_otziv

@bot.message_handler(content_types=['new_chat_members'])
def greeting(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	q = q.execute('SELECT * FROM chat_garant WHERE chat_id IS '+str(message.chat.id))
	row = q.fetchone()
	if row is None:
		bot.send_message(message.chat.id, f'''id чата: <code>{message.chat.id}</code>''' ,parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start_message(message):
	if message.chat.type == 'private':
		userid = str(message.chat.id)
		print(message.text)
		username = str(message.from_user.username)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute('SELECT * FROM ugc_users WHERE id IS '+str(userid))
		row = q.fetchone()
		if row is None:
			now = datetime.now()
			now_date = str(str(now)[:10])
			q.execute("INSERT INTO ugc_users (id,name,data_reg) VALUES ('%s', '%s', '%s')"%(userid,username,now_date))
			connection.commit()
			bot.send_message(message.chat.id,f'''💌 Добро пожаловать, @| <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>

❇️❗️🌐 Вас приветствует лучший бот-автогарант в телеграм, наблюдая за ботом SAVE CLICK, вы увидите еще много новвоведений, нацеленных на развитие бота и его дальнейшего функционала. 

🤖Моя цель - создать комфортную безопасную торговую среду для каждого пользователя.

💟Мы будем рады выслушать ваши пожелания по боту. Вопросы и предложения по улучшению SAVE CLICK вы так же можете задать:
@alexandrshcherbak

✨Следите за нами, вас ждет еще много нового!

💙Спасибо что остаетесь с нами.
💵Удачи в сделках!''',parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)
			if message.text[7:] != '':
				if message.text[7:] != message.chat.id:
					q.execute("update ugc_users set ref = " + str(message.text[7:])+ " where id = " + str(message.chat.id))
					connection.commit()
					q.execute("update ugc_users set ref_colvo =ref_colvo + 1 where id = " + str(message.text[7:]))
					connection.commit()
					bot.send_message(message.text[7:], f'Новый реферал! <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, f'''💌 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>

❇️❗️🌐 Вас приветствует лучший бот-автогарант в телеграм, наблюдая за ботом SAVE CLICK, вы увидите еще много новвоведений, нацеленных на развитие бота и его дальнейшего функционала. 

🤖Моя цель - создать комфортную безопасную торговую среду для каждого пользователя.

💟Мы будем рады выслушать ваши пожелания по боту. Вопросы и предложения по улучшению SAVE CLICK вы так же можете задать:
@alexandrshcherbak

✨Следите за нами, вас ждет еще много нового!

💙Спасибо что остаетесь с нами.
💵Удачи в сделках!''',parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)

@bot.message_handler(commands=['garant'])
def garant(message):
	try:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT balans FROM ugc_users where id is " + str(message.from_user.id))
		balanss = q.fetchone()
		if int(balanss[0]) >= int(message.text[8:].split(' ')[1]):
			q.execute("update ugc_users set balans = balans - "+str(message.text[8:].split(' ')[1])+" where id = " + str(message.from_user.id))
			connection.commit()
			foo = message.text[8:].split(' ')[0].upper() 
			foo = foo.replace("@", "")
			id_id = q.execute(f"SELECT id FROM ugc_users where name = '{foo.lower()}'").fetchone()[0]
			now = datetime.now()
			now_date = str(str(now)[:10])
			q.execute("INSERT INTO sdelki (user_create,user_invite,data,summa) VALUES ('%s', '%s', '%s', '%s')"%(message.from_user.id,id_id,now_date,message.text[8:].split(' ')[1]))
			connection.commit()
			user = message.text[8:].split(' ')[0]
			money = message.text[8:].split(' ')[1]
			q.execute(f"SELECT seq FROM sqlite_sequence where name = 'sdelki'")
			id_sdelka = q.fetchone()[0]
			bot.send_message(message.chat.id, f'''🔰  {user} у тебя новая сделка от @{message.from_user.username} на сумму {money} RUB, перейдите в @SAVEGARANT_bot -> 🤝 Мои сделки''',parse_mode='HTML')
			bot.send_message(message.chat.id, f'''🔰 Сделка #G{id_sdelka} от @{message.from_user.username} для @{user}

💰 Сумма сделки: {money} RUB''')
		else:
			bot.reply_to(message, '✖️ Недостаточно средств, перейдите в в @SAVEGARANT_bot -> 💻 Мой профиль')

	except:	
		bot.reply_to(message, '✖️ Пользователя нет в базе, попросите отправить любое сообщение в чат')


@bot.message_handler(content_types=['text'])
def send_text(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	q = q.execute('SELECT * FROM ugc_users WHERE id IS '+str(message.from_user.id))
	row = q.fetchone()
	if row is None:
		now = datetime.now()
		now_date = str(str(now)[:10])
		q.execute("INSERT INTO ugc_users (id,name,data_reg,chat_user) VALUES ('%s', '%s', '%s', '%s')"%(message.from_user.id,message.from_user.username.lower(),now_date,message.chat.id))
		connection.commit()
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	username = str(message.from_user.username.lower())
	q.execute(f"SELECT name FROM ugc_users where id = '{message.from_user.id}'")
	name = q.fetchone()
	if str(name[0]) == str(username):
		pass
	else:
		bot.reply_to(message, 'Ваш юзернейм обновлен')
		q.execute(f"update ugc_users set name = '{username}' where id = '{message.from_user.id}'")
		connection.commit()

	if message.chat.type == 'private':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		username = str(message.from_user.username.lower())
		q.execute(f"SELECT name FROM ugc_users where id = '{message.chat.id}'")
		name = q.fetchone()
		if str(name[0]) == str(username):
			pass
		else:
			bot.send_message(message.chat.id, 'Ваш юзернейм обновлен')
			q.execute(f"update ugc_users set name = '{username}' where id = '{message.chat.id}'")
			connection.commit()

		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT status FROM ugc_users where id is " + str(message.chat.id))
		status = q.fetchone()
		if str(status[0]) == str('Активен'):

			

			if message.text.lower() == '/admin':
				if message.chat.id == config.admin:
					msg = bot.send_message(message.chat.id, '<b>Привет, админ!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
					return

			elif message.text.lower() == 'gift':
				if message.chat.id == config.admin:
					msg= bot.send_message(message.chat.id, '''Приз
Колво сделок
Время''',parse_mode='HTML', reply_markup=keyboards.otmena)
					bot.register_next_step_handler(msg, add_gift)

			elif message.text.lower() == 'автопостинг':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("SELECT texts FROM avtopost  where id = "+str(1))
					texts = q.fetchone()[0]
					q.execute("SELECT timess FROM avtopost  where id = "+str(1))
					timess = q.fetchone()[0]
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Изменить текст',callback_data=f'изменитьтекст{1}'))
					keyboard.add(types.InlineKeyboardButton(text='Изменить задержку',callback_data=f'изменитьтекст{2}'))
					keyboard.add(types.InlineKeyboardButton(text='Изменить картинку',callback_data=f'изменитьтекст{3}'))
					bot.send_message(message.chat.id, f'''Текст:
{texts}


Задержка в секундах: {timess}''',parse_mode='HTML', reply_markup=keyboard)
					return

			elif message.text.lower() == 'настройки':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("SELECT com_sdelka FROM config  where id = "+str(1))
					com_sdelka = q.fetchone()[0]
					q.execute("SELECT com_vvod FROM config  where id = "+str(1))
					com_vvod = q.fetchone()[0]
					q.execute("SELECT id_arbtr FROM config  where id = "+str(1))
					id_arbtr = q.fetchone()[0]
					q.execute("SELECT com_vivod FROM config  where id = "+str(1))
					com_vivod = q.fetchone()[0]
					q.execute("SELECT uv_dep FROM config  where id = "+str(1))
					uv_dep = q.fetchone()[0]
					q.execute("SELECT uv_arb FROM config  where id = "+str(1))
					uv_arb = q.fetchone()[0]
					q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
					uv_sdelki = q.fetchone()[0]
					q.execute("SELECT uv_vivod FROM config  where id = "+str(1))
					uv_vivod = q.fetchone()[0]
					qiwi_phone = q.execute("SELECT qiwi_phone FROM config where id = '1'").fetchone()[0]
					qiwi_token = q.execute("SELECT qiwi_token FROM config where id = '1'").fetchone()[0]
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Изменить комиссию за пополнение',callback_data=f'изменитькоммисию{1}'))
					keyboard.add(types.InlineKeyboardButton(text='Изменить комиссию за сделки',callback_data=f'изменитькоммисию{3}'))
					keyboard.add(types.InlineKeyboardButton(text='Настроить уведомления',callback_data=f'уведомлениянастройка'))
					keyboard.add(types.InlineKeyboardButton(text='Изменить номер YA',callback_data='изменитьномер_'),types.InlineKeyboardButton(text='Изменить Token YA',callback_data='изменитьтокен_'))
					keyboard.add(types.InlineKeyboardButton(text='Сменить арбитра',callback_data=f'арбитры удалить{1}'))
					bot.send_message(message.chat.id, f'''Комиссия вывод: <code>{com_vivod}</code> %
Комиссия за сделки: <code>{com_sdelka}</code> %

Арбитры: <code>{id_arbtr}</code>
Номер YA: <code>{qiwi_phone}</code>
Токен YA: <code>{qiwi_token}</code>''',parse_mode='HTML', reply_markup=keyboard)
					return


			elif message.text.lower() == 'статистика':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					now = datetime.now()
					now_date = str(str(now)[:10])
					all_user_count = q.execute(f'SELECT COUNT(id) FROM ugc_users').fetchone()[0]
					new_user_count = q.execute(f'SELECT COUNT(id) FROM ugc_users WHERE data_reg = "{now_date}"').fetchone()[0]
					all_buys_count = q.execute(f'SELECT COUNT(id) FROM sdelki').fetchone()[0]
					new_buys_count = q.execute(f'SELECT COUNT(id) FROM sdelki WHERE data = "{now_date}"').fetchone()[0]
					all_earn_count = q.execute(f'SELECT SUM(summa) FROM sdelki').fetchone()[0]
					
					bot.send_message(message.chat.id, f'''Статистика проекта:
Всего пользователей: {all_user_count}
Новых за сегодня: {new_user_count}

Всего сделок: {all_buys_count}
Сделок за сегодня: {new_buys_count}

Сумма сделок: {all_earn_count}''')
					return

			elif message.text.lower() == 'выплаты':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					keyboard = types.InlineKeyboardMarkup()
					q.execute("SELECT * FROM vivod where status = 'on'")
					row = q.fetchall()
					for i in row:
						keyboard.add(types.InlineKeyboardButton(text=f'{i[2]} | {i[3]}', callback_data=f'vivod_{i[0]}'))

					bot.send_message(message.chat.id, "Выбери нуный: ", reply_markup=keyboard)
					return

			elif message.text.lower() == 'арбитражи':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					keyboard = types.InlineKeyboardMarkup()
					q.execute("SELECT * FROM sdelki where status = 'Арбитраж'")
					row = q.fetchall()
					for i in row:
						keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=f'aaadddd_{i[0]}'))

					bot.send_message(message.chat.id, "Выбери нужный: ", reply_markup=keyboard)
					return

			elif message.text.lower() == '/arb':
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("SELECT id_arbtr FROM config  where id = "+str(1))
				bot_ad = q.fetchone()[0]
				if message.chat.id == bot_ad:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					keyboard = types.InlineKeyboardMarkup()
					q.execute("SELECT * FROM sdelki where status = 'Арбитраж'")
					row = q.fetchall()
					for i in row:
						keyboard.add(types.InlineKeyboardButton(text=i[0], callback_data=f'aaadddd_{i[0]}'))
					bot.send_message(message.chat.id, "Выбери нужный: ", reply_markup=keyboard)
					return


			elif message.text.lower() == 'cделки':
				if message.chat.id == config.admin:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute(f"SELECT * FROM sdelki")
					info = q.fetchall()
					rand = random.randint(10000000,99999999999)
					keyboard = types.InlineKeyboardMarkup()
					for i in info:
						q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
						iduser_sellname = q.fetchone()[0]
						q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
						idubuyname = q.fetchone()[0]
						doc = open(f'G{rand}.txt', 'a', encoding='utf8')
						doc.write(f'''ID: #G{i[0]} | Покупатель: @{idubuyname} | Продавец: @{iduser_sellname} | Cумма: {i[6]} | Дата {i[3]} | Статус: {i[5]} \n''')
						doc.close()
					try:
						file = open(f'G{rand}.txt', encoding='utf8')
						bot.send_document(message.chat.id,file, caption='Cделки')
						file.close()
						os.remove(f'G{rand}.txt')
					except:
						bot.send_message(message.chat.id, 'Сделки отсутствуют', reply_markup=keyboards.admin)
					return



			elif message.text.lower() == 'пользователи':
				if message.chat.id == config.admin:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Найти пользователя',callback_data='admin_search_user'))
					bot.send_message(message.chat.id, '<b>Нажми на кнопку</b>',parse_mode='HTML', reply_markup=keyboard)
					return

			elif message.text.lower() == 'рассылка':
				if message.chat.id == config.admin:
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='С картинокй',callback_data=f'Рассылка{1}'))
					keyboard.add(types.InlineKeyboardButton(text='С гиф',callback_data=f'Рассылка{2}'))
					keyboard.add(types.InlineKeyboardButton(text='С видео',callback_data=f'Рассылка{3}'))
					bot.send_message(message.chat.id, f'''как будем рассылкать ?''',parse_mode='HTML', reply_markup=keyboard)
					return

			elif message.text.lower() == '🔰 интеграция в чат':
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Что это такое ⁉️',callback_data='инфочат'))
				keyboard.add(types.InlineKeyboardButton(text='➕ Добавить в чат',callback_data='добавитьвчат'))
				bot.send_message(message.chat.id, '''🚪Вы попали в меню интеграции бота в чат. 

⏳💰🛡🤝Больше не нужно опасаться скамеров в чате и искать гарантов с бешенными процентами, отныне бота SAVE CLICK можно внедрять в любой чат телеграм.

⚠️В чате должно быть от 300 участников.''', reply_markup=keyboard)
				return


			elif message.text.lower() == '🤝 мои сделки':
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🔐Активные сделки',callback_data='my_sdelki'),types.InlineKeyboardButton(text='🔒Закрытые сделки',callback_data='закрытыесделки'))
				bot.send_message(message.chat.id, "Какие сделки вас интересуют: ", reply_markup=keyboard)
				return

			elif message.text.lower() == '🔍 открыть сделку':
				msg = bot.send_message(message.chat.id, f'Введите никнейм в формате @username (как в профиле)',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg,searchuser)
				return

			elif message.text.lower() == '🌐 информация':
				keyboard = types.InlineKeyboardMarkup()
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("SELECT url_ard FROM config  where id = "+str(1))
				url_ard = q.fetchone()[0]
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🧑‍⚖️ Написать арбитру',url=url_ard))
				keyboard.add(types.InlineKeyboardButton(text='🗯 Чат пользователей ',url=f'https://t.me/joinchat/U7--P7Z7'))
				bot.send_message(message.chat.id, f'''<b>Пользователи сервиса могут провести сделку 24/7, что, согласитесь, очень удобно.

Основные моменты:</b><i>
➖ Минимальная сумма сделки 10 RUB
➖ Оплата принимается в BTC BANKIR и QIWI. Выплата, соответственно, производится также
➖ Комиссия сервиса 7%
➖ Сумма сделки фиксируется в RUB в момент заключения сделки.</i>

<b>Открытие спора после оплаты Гарант-Сервиса.</b>
<i>➖ У покупателя и у продавца в процессе сделки есть кнопка "Открыть арбитраж". Сделка автоматически переходит в статус "Арбитраж". Продавец или покупатель должны написать Арбитру. После вынесения решения - денежные средства переводятся.</i>


<b>Внимание! Сделку должен начать Покупатель воспользовавшись поиском пользователей! Это важный момент.</b>''' ,parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)
				return
			elif message.text.lower() == '📖 f.a.q':
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🧑‍⚖️ Написать арбитру',url='https://t.me/'))
				keyboard.add(types.InlineKeyboardButton(text='🗯 Чат пользователей ',url=f'https://t.me//U7--P7Z7'))
				bot.send_message(message.chat.id, f'''📖Схема работы бота построена следующим образом:

1. ✅Покупатель пополняет свой счет в боте любым доступным и удобным для себя способом.
2. ✅Покупатель нажимает кнопку «открыть сделку».
3. ✅Покупателю высвечивается окно ввода юзернейма продавца для приглашения в сделку.
4. ✅После ввода юзернейма покупателю необходимо указать сумму сделки. Покупатель может прописать условия сделки, если они есть, или же выбрать сделку без обязательств.
5. ✅После подтверждения покупателем, продавцу приходит уведомление о новом этапе сделки, а покупатель может ожидать свой товар для последующей проверки.
6. ✅Если условия сделки соблюдены и покупателя устроил товар - необходимо отпустить средства.
7. ✅Продавцу приходит уведомление о успешном завершении сделки, после чего продавец имеет возможность вывести средства любым удобным способом.
🔁 Комиссия бота составляет: 7%.

🆘🛃В случае если покупатель хочет оспорить сделку, если условия не соответствуют оговоренными в сделке, либо же покупателя пытаются обмануть, ему необходимо нажать кнопку «открыть арбитраж», в таком случае модераторы SAVE CLICK отменят сделку в пользу покупателя в течении 10 минут с момента создания заявки.

❗️Внимание! Сделку должен начать Покупатель воспользовавшись поиском пользователей! Это важный момент.

🤗Удачи в сделках!''',parse_mode='HTML', reply_markup=keyboard)
				return

			elif message.text.lower() == '🚫 scam list':
				msg = bot.send_message(message.chat.id, f'Введите никнейм в формате @username или id пользователя',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg,poisk_scam)


				return
			elif message.text.lower() == '🎲 игры':
				bot.send_message(message.chat.id, f'''⏳ В разработке......''',parse_mode='HTML', reply_markup=keyboards.main)
				return



			elif message.text.lower() == '💻 мой профиль':
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("SELECT balans FROM ugc_users where id is " + str(message.chat.id))
				balanss = q.fetchone()
				q.execute("SELECT data_reg FROM ugc_users where id is " + str(message.chat.id))
				data_reg = q.fetchone()
				q.execute("SELECT raiting FROM ugc_users where id is " + str(message.chat.id))
				raiting = q.fetchone()
				q.execute("SELECT sdelka_colvo FROM ugc_users where id is " + str(message.chat.id))
				sdelka_colvo = q.fetchone()
				q.execute("SELECT sdelka_summa FROM ugc_users where id is " + str(message.chat.id))
				sdelka_summa = q.fetchone()
				balance = balanss[0]
				curse = requests.get(f'https://blockchain.info/tobtc?currency=RUB&value={balance}').text
				urse = requests.get(f'https://blockchain.info/tobtc?currency=RUB&value={sdelka_summa[0]}').text
				covlotziv = q.execute(f'SELECT COUNT(id) FROM otziv  where user = {message.chat.id}').fetchone()[0]

				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='🔺Пополнить',callback_data=f'awhat_oplata'),types.InlineKeyboardButton(text='🔻Вывести',callback_data=f'awhat_wind'))
				keyboard.add(types.InlineKeyboardButton(text='👥 Партнерская программа',callback_data='fereralka'))
				keyboard.add(types.InlineKeyboardButton(text='🎁 Ваучеры',callback_data='vau'))

				bot.send_message(message.chat.id, f'''
🆔 Ваш ID: <code>{message.chat.id}</code>

💰 Баланс: <code>{balance}</code> RUB | <code>{curse}</code> BTC

📋 Количество сделок: <code>{sdelka_colvo[0]}</code>

💎 Сумма сделок: <code>{sdelka_summa[0]}</code> RUB | <code>{urse}</code> BTC

📊 Рейтинг: <code>{raiting[0]}</code> | 📮 Отзывов: <code>{covlotziv}</code>

🗓 Дата регистрации: {data_reg[0]}
''',parse_mode='HTML', reply_markup=keyboard)
				return


			bot.send_message(message.chat.id, '✖️ Команда не найдена !',parse_mode='HTML', reply_markup=keyboards.main)	

def poisk_scam(message):
	name_scam = message.text
	if name_scam != 'Отмена':
		try:
			if len(name_scam) >= 5:
				name_scam = name_scam.lower()
				connection = sqlite3.connect('scamlist.sqlite')
				q = connection.cursor()
				q.execute("SELECT * FROM scamlist")
				row = q.fetchall()
				for i in row:
					word = i[1].lower()
					counter = len(word.split(name_scam))-1
					if int(counter) >= 1:
						bot.send_message(message.chat.id, i[1],parse_mode='HTML', reply_markup=keyboards.main)
						bot.send_message(message.chat.id, '🚫 Возможно пользователь в scam листе, пост выше ⬆️',parse_mode='HTML', reply_markup=keyboards.main)
						return
				bot.send_message(message.chat.id, '✅ Ничего не найдено',parse_mode='HTML', reply_markup=keyboards.main)
			else:
				bot.send_message(message.chat.id, 'Аргументы указаны неверно!',parse_mode='HTML', reply_markup=keyboards.main)
		except:
			bot.send_message(message.chat.id, 'Аргументы указаны неверно!',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',parse_mode='HTML', reply_markup=keyboards.main)

	
def add_gift(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✅ Учавствовать',callback_data=f'участвоватьгифт'))
		try:
			q.execute("INSERT INTO add_guft (priz,colvo,time) VALUES ('%s','%s','%s')"%(message.text.split('\n')[0],message.text.split('\n')[1],message.text.split('\n')[2]))
			connection.commit()
			time = int(message.text.split('\n')[2])/ 60
			prizz = message.text.split('\n')[0]
			colvosdelokkk = message.text.split('\n')[1]
			q.execute("SELECT * FROM ugc_users")
			row = q.fetchall()
			for i in row:
				try:
					bot.send_message(i[0], f'''❗️ Дамы и господа, внимание ❗️

⭐️⭐️⭐️Розыгрыш⭐️⭐️⭐️

💰 Сумма розыгрыша: {prizz}
🤝 Количество сделок в боте: {colvosdelokkk}
⏳ Время розыгрыша: {time} мин''', reply_markup=keyboard)
				except:
					pass

			bot.send_message(message.chat.id, 'ГОТОВО', reply_markup=keyboards.admin)
		except Exception as e:
			bot.send_message(message.chat.id, 'Ошибка', reply_markup=keyboards.admin)
		
	else:
		msg = bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.admin)

def new_chat(message):
	new_categ = message.text
	if new_categ != 'Отмена':
		try:
			bot.send_message(new_categ, '✔️ Теперь все сделки строго через меня',parse_mode='HTML')
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q = q.execute('SELECT * FROM chat_garant WHERE chat_id IS '+str(new_categ))
			row = q.fetchone()
			if row is None:
				q.execute("INSERT INTO chat_garant (chat_id,user) VALUES ('%s', '%s')"%(new_categ,message.chat.id))
				connection.commit()
				bot.send_message(message.chat.id, '✔️ Вы успешно подключили чат.  теперь вся комиссия за участников чата будет приходить к вам на баланс !',parse_mode='HTML', reply_markup=keyboards.main)
			else:
				bot.send_message(message.chat.id, '✖️ Ошибка, бот уже добавлен в данный чат.',parse_mode='HTML', reply_markup=keyboards.main)

		except:
			bot.send_message(message.chat.id, '✖️ Ошибка, бот не админ или чат указан неверно ',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',parse_mode='HTML', reply_markup=keyboards.main)

def new_admin(message):
	new_categ = message.text
	if new_categ != 'Отмена':
		try:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute(f"update config set id_arbtr = '{message.text}'")
			connection.commit()		
			connection.close()
			bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
		except:
			bot.send_message(message.chat.id, 'Аргументы указаны неверно!',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',parse_mode='HTML', reply_markup=keyboards.admin)

def searchuser(message):
	if message.text.lower() != 'отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		foo = message.text.upper() 
		foo = foo.replace("@", "")
		q.execute(f"SELECT * FROM ugc_users where upper(name) = '{foo}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.main)
		username = str(message.from_user.username)
		if row != None:
			if str(username) == str(row[1]):
				keyboard = types.InlineKeyboardMarkup()
				q.execute(f"SELECT name FROM ugc_users where id = '{row[0]}'")
				iduser_sellname = q.fetchone()[0]
				urse = requests.get(f'https://blockchain.info/tobtc?currency=RUB&value={row[7]}').text
				covlotziv = q.execute(f'SELECT COUNT(id) FROM otziv  where user = {row[0]}').fetchone()[0]
				keyboard.add(types.InlineKeyboardButton(text=f'📜 Отзывы ({covlotziv} шт.)',callback_data=f'отзывысмотреть{row[0]}'))
				msg = bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

👤 Пользователь: @{iduser_sellname}

📋 Количество сделок: <code>{row[6]}</code>

💎 Сумма сделок: <code>{row[7]}</code> RUB | <code>{urse}</code> BTC

📊 Рейтинг: <code>{row[5]}</code> | 📮Отзывов: <code>{covlotziv}</code>

🗓 Дата регистрации: {row[10]}
	''',parse_mode='HTML', reply_markup=keyboard)
			else:
				keyboard = types.InlineKeyboardMarkup()
				q.execute(f"SELECT name FROM ugc_users where id = '{row[0]}'")
				iduser_sellname = q.fetchone()[0]
				urse = requests.get(f'https://blockchain.info/tobtc?currency=RUB&value={row[7]}').text
				covlotziv = q.execute(f'SELECT COUNT(id) FROM otziv  where user = {row[0]}').fetchone()[0]
				keyboard.add(types.InlineKeyboardButton(text='🔰 Открыть сделку',callback_data=f'Открытьсделку{row[0]}'))
				keyboard.add(types.InlineKeyboardButton(text=f'📜 Отзывы ({covlotziv} шт.)',callback_data=f'отзывысмотреть{row[0]}'))
				msg = bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

👤 Пользователь: @{iduser_sellname}

📋 Количество сделок: <code>{row[6]}</code>

💎 Сумма сделок: <code>{row[7]}</code> RUB | <code>{urse}</code> BTC

📊 Рейтинг: <code>{row[5]}</code> | 📮Отзывов: <code>{covlotziv}</code>

🗓 Дата регистрации: {row[10]}
	''',parse_mode='HTML', reply_markup=keyboard)

		else:
			bot.send_message(message.chat.id, '<b>Мы не нашли такого пользователя в базе!</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.main)

def searchuserss(message):
	if message.text.lower() != 'отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM ugc_users where upper(name) = '{message.text.upper()}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.main)
		username = str(message.from_user.username)
		if row != None:
			q.execute(f"SELECT name FROM ugc_users where id = '{row[0]}'")
			iduser_sellname = q.fetchone()[0]
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='➕ Изменить баланс',callback_data=f'добавитьбаланс_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='🔒 Заблокировать | Раблокировать',callback_data=f'заблокировать_{row[0]}'))
			bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

<b>👤 Пользователь:</b> @{iduser_sellname}

<b>♻️ Количество сделок:</b> <code>{row[6]}</code>

<b>💳 Сумма сделок:</b> <code>{row[7]}</code>

<b>📊 Рейтинг:</b> <code>{row[5]}</code>

<b>Статус:</b> <code>{row[8]}</code>
''',parse_mode='HTML', reply_markup=keyboard)

		else:
			bot.send_message(message.chat.id, '<b>Мы не нашли такого пользователя в базе!</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.main)

def btc_oplata_1(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		if "https://telegram.me/BTC_CHANGE_BOT?" in str(message.text):
			q.execute("INSERT INTO BTC_CHANGE_BOT (text,user) VALUES ('%s','%s')"%(message.text,message.chat.id))
			connection.commit()
			bot.send_message(message.chat.id, '💰 Чек проверяется, примерное время проверки 1 минута, вам придет уведомление.', reply_markup=keyboards.main)
			return
		if "https://telegram.me/LTC_CHANGE_BOT?" in str(message.text):
			q.execute("INSERT INTO LTC_CHANGE_BOT (text,user) VALUES ('%s','%s')"%(message.text,message.chat.id))
			connection.commit()
			bot.send_message(message.chat.id, '💰 Чек проверяется, примерное время проверки 1 минута, вам придет уведомление.', reply_markup=keyboards.main)
			return
		if "https://telegram.me/ETH_CHANGE_BOT?" in str(message.text):
			q.execute("INSERT INTO ETH_CHANGE_BOT (text,user) VALUES ('%s','%s')"%(message.text,message.chat.id))
			connection.commit()
			bot.send_message(message.chat.id, '💰 Чек проверяется, примерное время проверки 1 минута, вам придет уведомление.', reply_markup=keyboards.main)
			return
		else:

			msg = bot.send_message(message.chat.id, f'✖️ Чек указан неверно!', reply_markup=keyboards.main)
	else:
		msg = bot.send_message(message.chat.id, '✖️ Вернулись на главную', reply_markup=keyboards.main)

def comsaedit(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"update config set {str(comsa)} = '{message.text}' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def postedit(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"update avtopost set {str(idtexts)} = '{message.text}' where id = '1'")
		connection.commit()
		cmd = 'systemctl stop test.service'
		subprocess.Popen(cmd, shell=True)
		cmdd = 'systemctl start test.service'
		subprocess.Popen(cmdd, shell=True)
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)


def smena_id_uv(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"update config set {str(conf_uvs)} = '{message.text}' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)


def send_photoorno(message):
	if message.text != 'Отмена':
		global text_send_all
		text_send_all = message.text
		msg = bot.send_message(message.chat.id, 'Отправьте ссылку на медиа',parse_mode='HTML',disable_web_page_preview = True)
		bot.register_next_step_handler(msg, admin_send_message_all_text_rus)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)


def admin_send_message_all_text_rus(message):
	if message.text != 'Отмена':
		global media
		media = message.text
		if int(tipsend) == 1:
			msg = bot.send_photo(message.chat.id,str(media), "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
				
		if int(tipsend) == 2:
			print(tipsend)
			msg = bot.send_animation(chat_id=message.chat.id, animation=media, caption="Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

		if int(tipsend) == 3:
			print(tipsend)
			media = f'<a href="{media}">.</a>'
			msg = bot.send_message(message.chat.id, f'''Отправить всем пользователям уведомление:
{text_send_all}
{media}
Если вы согласны, напишите Да''',parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def admin_send_message_all_text_da_rus(message):
	otvet = message.text
	colvo_send_message_users = 0
	colvo_dont_send_message_users = 0
	if message.text != 'Отмена':	
		if message.text.lower() == 'Да'.lower():
			connection = sqlite3.connect('database.sqlite')
			with connection:	
				q = connection.cursor()
				bot.send_message(message.chat.id, 'Начинаем отправлять!')
				if int(tipsend) == 1: # картинка
					q.execute("SELECT * FROM ugc_users")
					row = q.fetchall()
					for i in row:
						jobid = i[0]

						time.sleep(0.1)
						reply = json.dumps({'inline_keyboard': [[{'text': '✖️ Закрыть', 'callback_data': f'restart'}]]})
						response = requests.post(
							url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendPhoto"),
							data={'chat_id': jobid,'photo': str(media), 'caption': str(text_send_all),'reply_markup': str(reply),'parse_mode': 'HTML'}
						).json()
						if response['ok'] == False:
							colvo_dont_send_message_users = colvo_dont_send_message_users + 1
						else:
							colvo_send_message_users = colvo_send_message_users + 1;
					bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	

				elif int(tipsend) == 2: # гиф
					q.execute("SELECT * FROM ugc_users")
					row = q.fetchall()
					for i in row:
						jobid = i[0]

						time.sleep(0.1)
						reply = json.dumps({'inline_keyboard': [[{'text': '✖️ Закрыть', 'callback_data': f'restart'}]]})
						response = requests.post(
							url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendAnimation"),
							data={'chat_id': jobid,'animation': str(media), 'caption': str(text_send_all),'reply_markup': str(reply),'parse_mode': 'HTML'}
						).json()
						if response['ok'] == False:
							colvo_dont_send_message_users = colvo_dont_send_message_users + 1
						else:
							colvo_send_message_users = colvo_send_message_users + 1;
					bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	


				elif int(tipsend) == 3: # видео
					q.execute("SELECT * FROM ugc_users")
					row = q.fetchall()
					for i in row:
						jobid = i[0]
						time.sleep(0.2)
						response = requests.post(
							url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendMessage"),
							data={'chat_id': jobid, 'text': str(text_send_all) + str(media),'parse_mode': 'HTML'}
						).json()
						if response['ok'] == False:
							colvo_dont_send_message_users = colvo_dont_send_message_users + 1
						else:
							colvo_send_message_users = colvo_send_message_users + 1;
					bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)				



def add_money2(message):
   if message.text != 'Отмена':
      connection = sqlite3.connect('database.sqlite')
      q = connection.cursor()
      q.execute("update ugc_users set balans = balans +" + str( message.text ) +  " where id =" + str(id_user_edit_bal1))
      connection.commit()
      msg = bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)




def create_sdelka1(message):
	opisaniesdelka = message.text
	if message.text.isdigit() == True and int(message.text) >= 10:
		if opisaniesdelka != 'Отмена':
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				balanss = q.execute("SELECT balans FROM ugc_users where id is " + str(message.chat.id)).fetchone()[0]
				if int(balanss) >= int(message.text):
					q.execute(f"update ugc_users set balans = balans - '{message.text}' where id = '{message.chat.id}'")
					connection.commit()
					now = datetime.now()
					now_date = str(str(now)[:10])
					q.execute("INSERT INTO sdelki (user_create,user_invite,data,summa) VALUES ('%s', '%s', '%s', '%s')"%(message.chat.id,iduser_sell,now_date,opisaniesdelka))
					connection.commit()
					q.execute(f"SELECT name FROM ugc_users where id = '{iduser_sell}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{message.chat.id}'")
					idubuyname = q.fetchone()[0]
					q.execute(f"SELECT seq FROM sqlite_sequence where name = 'sdelki'")
					id_sdelka = q.fetchone()[0]
					q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
					uv_sdelki = q.fetchone()[0]
					bot.send_message(uv_sdelki, f'''🔰 Сделка #G{id_sdelka} от @{idubuyname} для @{iduser_sellname}

💰 Сумма сделки: {message.text} RUB''')
					bot.send_message(message.chat.id, f'''🔰 Сделка: #G{id_sdelka} успешно создана, продавец получил оповещение, ожидайте товар.''',parse_mode='HTML', reply_markup=keyboards.main)

					bot.send_message(iduser_sell, f'''🔰 Поступила сделка от <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>
💰 Сумма сделки: <code>{message.text}</code> RUB

Чтобы отказаться от сделки
или открыть спор - перейдите в раздел 
🤝 Мои сделки >> 🔐Активные сделки''',parse_mode='HTML', reply_markup=keyboards.main)
				else:
					bot.send_message(message.chat.id, '❌ Недостаточно средств на балансе!',parse_mode='HTML', reply_markup=keyboards.main)

		else:
			bot.send_message(message.chat.id, 'Вернулись на главную',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '✖️ Вводить нужно число\nПовторите попытку', reply_markup=keyboards.main)





def vau_add(message):
	if message.content_type == 'text':
		if message.text.isdigit() == True and int(message.text) >= 1 and int(message.text) <= 99999999999999:
			if message.text != 'Отмена':
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				if message.text.isdigit() == True:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
					check_balans = q.fetchone()
					if float(check_balans[0]) >= int(message.text):
							colvo = 1
							dlina = 10
							chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
							for ttt in range(1):
								for n in range(10):
									id_sdelka =''
								for i in range(int(dlina)):
									id_sdelka += random.choice(chars)
							print(id_sdelka)
							q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
							connection.commit()
							q.execute("INSERT INTO vau (name,summa,adds) VALUES ('%s', '%s', '%s')"%(id_sdelka,message.text,message.chat.id))
							connection.commit()
							bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{id_sdelka}</code>, успешно создан.''',reply_markup=keyboards.main, parse_mode='HTML')
							q.close()
							connection.close()
					else:
						msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

				else:
					msg = bot.send_message(message.chat.id, '⚠ Ошибка!')
			else:
				bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, '✖️ Не правильно указана сумма.',parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, '✖️ Вводить нужно число\nПовторите попытку', reply_markup=keyboards.main)
def new_token(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set qiwi_token = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_phone(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set qiwi_phone = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def yo_viplata(message):
	qiwi_user = message.text
	if message.text != '🔶 Отменить':
		if qiwi_user[:1] == '4' and len(qiwi_user) == 16:
			if qiwi_user.isdigit() == True:
				global numberphone
				numberphone = message.text
				msg = bot.send_message(message.chat.id, 'Введите сумму для выплаты')
				bot.register_next_step_handler(msg, yo_vilata_card)
			else:
				bot.send_message(message.chat.id, '📛 Неверно указан номер карты!',reply_markup=keyboards.main)
		else:
			msg = bot.send_message(message.chat.id, '📛 Неверно указан номер карты!')

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def yo_vilata_card(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT com_vivod FROM config  where id = "+str(1))
		com_vivod = q.fetchone()[0]
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = com_vivod
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("INSERT INTO vivod (user_id,summa,method,rek) VALUES ('%s', '%s', '%s', '%s')"%(message.chat.id,sum_vivod, 'Yandex',numberphone))
				connection.commit()
				bot.send_message(message.chat.id, '''✅ Выплата успешно заказана, ожидайте перевод !''',reply_markup=keyboards.main, parse_mode='HTML')
				q.close()
				connection.close()
		else:
			msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

	else:
		msg = bot.send_message(message.chat.id, '⚠ Ошибка!')

def card_viplata(message):
	qiwi_user = message.text
	if message.text != '🔶 Отменить':
		if qiwi_user[:1] == '4' and len(qiwi_user) == 16 or qiwi_user[:1] == '5' and len(qiwi_user) == 16:
			if qiwi_user.isdigit() == True:
				global numberphone
				numberphone = message.text
				msg = bot.send_message(message.chat.id, 'Введите сумму для выплаты')
				bot.register_next_step_handler(msg, summa_vilata_card)
			else:
				bot.send_message(message.chat.id, '📛 Неверно указан номер карты!',reply_markup=keyboards.main)
		else:
			msg = bot.send_message(message.chat.id, '📛 Неверно указан номер карты!')

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def summa_vilata_card(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT com_vivod FROM config  where id = "+str(1))
		com_vivod = q.fetchone()[0]
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = com_vivod
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("INSERT INTO vivod (user_id,summa,method,rek) VALUES ('%s', '%s', '%s', '%s')"%(message.chat.id,sum_vivod, 'CARD',numberphone))
				connection.commit()
				bot.send_message(message.chat.id, '''✅ Выплата успешно заказана, ожидайте перевод !''',reply_markup=keyboards.main, parse_mode='HTML')
				q.close()
				connection.close()
		else:
			msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

	else:
		msg = bot.send_message(message.chat.id, '⚠ Ошибка!')

def btc_viplata(message):
	qiwi_user = message.text
	if message.text != '🔶 Отменить':
		global numberphone
		numberphone = message.text
		msg = bot.send_message(message.chat.id, 'Введите сумму для выплаты')
		bot.register_next_step_handler(msg, summa_vilata_btc)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)


def otziv_2_2(message):
	if message.text != 'Отмена':
		try:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute(f"SELECT name FROM ugc_users where id = '{awfawfawaaa}'")
			iduser_sellname = q.fetchone()[0]
			q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
			uv_sdelki = q.fetchone()[0]
			covlotziv = q.execute(f'SELECT COUNT(id) FROM otziv where user = {awfawfawaaa}').fetchone()[0]
			print()
			covlotziv = int(covlotziv) + 1
			q.execute("INSERT INTO otziv (user,texts,otsuser,id_otziv) VALUES ('%s', '%s', '%s', '%s')"%(awfawfawaaa,message.text,f'@{message.from_user.username}',covlotziv))
			connection.commit()
			bot.send_message(uv_sdelki, f'''Получен отзыв! 
От @{message.from_user.username} для @{iduser_sellname} по сделке #G{id_sdelka_otziv}
----- 

{message.text}
''', parse_mode='HTML')
			bot.send_message(message.chat.id, f'❤️ Спасибо за отзыв',reply_markup=keyboards.main)
		except Exception as e:
			print(e)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def summa_vilata_btc(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT com_vivod FROM config  where id = "+str(1))
		com_vivod = q.fetchone()[0]
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = com_vivod
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("INSERT INTO vivod (user_id,summa,method,rek) VALUES ('%s', '%s', '%s', '%s')"%(message.chat.id,sum_vivod, 'BTC','0'))
				connection.commit()
				bot.send_message(message.chat.id, '''✅ Выплата успешно заказана, ожидайте перевод !''',reply_markup=keyboards.main, parse_mode='HTML')
				q.close()
				connection.close()
		else:
			msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

	else:
		msg = bot.send_message(message.chat.id, '⚠ Ошибка!')

def send_user(message):
	if message.text != 'Отмена':
		bot.send_message(message.chat.id, 'Готово !',reply_markup=keyboards.admin)
		bot.send_message(id_user_viplata, message.text,reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def qiwi_viplata(message):
	qiwi_user = message.text
	if message.text != 'Отмена':
		if qiwi_user[:1] == '7' and len(qiwi_user) == 11 or qiwi_user[:3] == '380' and len(qiwi_user[3:]) == 9 or qiwi_user[:3] == '375' and len(qiwi_user) <= 12:
			if qiwi_user.isdigit() == True:
				global numberphone
				numberphone = message.text
				msg = bot.send_message(message.chat.id, 'Введите сумму для выплаты')
				bot.register_next_step_handler(msg, summa_vilata_qiwi)
			else:
				bot.send_message(message.chat.id, '📛 Неверно указан кошелек!',reply_markup=keyboards.main)
		else:
			msg = bot.send_message(message.chat.id, '📛 Неверно указан кошелек!',reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def summa_vilata_qiwi(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		com_vivod = q.execute("SELECT com_vivod FROM config  where id = '1'").fetchone()[0]
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = com_vivod
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("INSERT INTO vivod (user_id,summa,method,rek) VALUES ('%s', '%s', '%s', '%s')"%(message.chat.id,sum_vivod, 'qiwi',numberphone))
				connection.commit()
				bot.send_message(message.chat.id, '''✅ Выплата успешно заказана, ожидайте перевод !''',reply_markup=keyboards.main, parse_mode='HTML')
				q.close()
				connection.close()
		else:
			msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

def proverka_ya(message):
	if message.text != 'Отмена':
		if message.text.isdigit() == True:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			qiwi_token = q.execute("SELECT qiwi_token FROM config where id = '1'").fetchone()[0]
			headers = {"Content-Type": "application/x-www-form-urlencoded","Authorization": f"Bearer {qiwi_token}"}
			code_req = requests.post('https://yoomoney.ru/api/operation-history', data=f'type=deposition&details=true', allow_redirects=False, headers=headers).json()
			for i in code_req['operations']:
				q = q.execute("SELECT id FROM temp_pay WHERE txnid = " + str(i['operation_id']))
				temp_pay = q.fetchone()
				if i['status'] == 'success' and i['amount_currency'] == 'RUB' and temp_pay == None:
					if int(message.text) == int(i['amount']):
						q.execute("INSERT INTO temp_pay (txnid) VALUES ('%s')"%(i['operation_id']))
						connection.commit()
						q.execute("update ugc_users set balans = balans + "+str(float(i['amount']))+" where id = " + str(message.chat.id))
						connection.commit()
						bot.send_message(message.chat.id, f"✅ На ваш баланс зачислено {i['amount']} RUB",parse_mode='HTML',reply_markup=keyboards.main)
						return
			bot.send_message(message.chat.id, f"⚠ Оплата не найдена!",parse_mode='HTML',reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, 'Ошибка',reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def vau_good(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM vau where name = '{message.text}'")
		status = q.fetchone()
		if status != None:
			print("yes")
			q.execute(f"SELECT summa FROM vau where name = '{message.text}'")
			summa = q.fetchone()
			q.execute(f"SELECT adds FROM vau where name = '{message.text}'")
			adds = q.fetchone()
			q.execute("update ugc_users set balans = balans + "+str(summa[0])+" where id = " + str(message.chat.id))
			connection.commit()
			print(summa[0])
			q.execute(f"DELETE FROM vau WHERE name = '{message.text}'")
			connection.commit()
			bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{message.text}</code>, успешно активирован. Ваш баланс пополнен на <code>{summa[0]}</code> RUB. ''',reply_markup=keyboards.main, parse_mode='HTML')
			bot.send_message(adds[0], f'''👤  <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>  активировал(а) ваучер <code>{message.text}</code>.''',reply_markup=keyboards.main, parse_mode='HTML')

		else:
			bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{message.text}</code>, не сушествует или уже активирован.''',reply_markup=keyboards.main, parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)
				
@bot.callback_query_handler(func=lambda call:True)
def podcategors(call):

	if call.data[:9] == 'my_sdelki':
		if call.data[9:] == '':
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🛃Как покупатель',callback_data='my_sdelki_buyer'))
			keyboard.add(types.InlineKeyboardButton(text='🛂Как продавец',callback_data='my_sdelki_seller'))
			bot.send_message(call.message.chat.id, 'Выбери тип сделки', reply_markup=keyboard)

		elif call.data[9:] == '_seller':
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute(f"SELECT * FROM sdelki where user_invite = '{call.message.chat.id}'")
			info = q.fetchall()
			if info != None:
				keyboard = types.InlineKeyboardMarkup()
				for i in info:
					if str(i[5]) == str('Финал'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотр сделки{i[0]}'))
					if str(i[5]) == str('Оплачена'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотр сделки{i[0]}'))
					if str(i[5]) == str('Арбитраж'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотр сделки{i[0]}'))
				bot.send_message(call.message.chat.id, f'''Выберите сделку''', parse_mode='HTML', reply_markup=keyboard)
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="У вас нет сделок такого типа")


		elif call.data[9:] == '_buyer':
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute(f"SELECT * FROM sdelki where user_create = '{call.message.chat.id}'")
			info = q.fetchall()
			if info != None:
				keyboard = types.InlineKeyboardMarkup()
				for i in info:
					if str(i[5]) == str('Финал'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Оплачена'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
					if str(i[5]) == str('Арбитраж'):
						keyboard.add(types.InlineKeyboardButton(text=f'🔰 Сделка:  #{i[0]} | {i[6]} ',callback_data=f'просмотрсделки{i[0]}'))
				bot.send_message(call.message.chat.id, f'''Выберите сделку''', parse_mode='HTML', reply_markup=keyboard)
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="У вас нет сделок такого типа")


	if call.data[:12] == 'awhat_oplata':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup(row_width=2)
		keyboard.add(types.InlineKeyboardButton(text=f'ЮMoney',callback_data=f'Depoziit_qiwi'),types.InlineKeyboardButton(text=f'💱 BTC|ETH|LTC Чек',callback_data=f'бткчек'))
		bot.send_message(call.message.chat.id,  'Выбери способ для депозита', reply_markup=keyboard)

	if call.data[:13] == 'Depoziit_qiwi':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		qiwi_phone = q.execute("SELECT qiwi_phone FROM config where id = '1'").fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✅ Проверить',callback_data='Check_Depozit_qiwi_'))
		bot.send_message(call.message.chat.id,f'''👉 Для пополнения баланса бота выполните рублёвый перевод на любую сумму по следующим реквизитам:

▫️ Кошелёк: <code>{qiwi_phone}</code>

⏱ После перевода нажмите кнопку "ПРОВЕРИТЬ" и укажите точную сумму платежа.''',parse_mode='HTML', reply_markup=keyboard)
		


	if call.data == 'Check_Depozit_qiwi_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id,f"<b>ℹ️ Укажите точную сумму платежа (Например - 100)</b>", reply_markup=keyboards.main, parse_mode='HTML')
		bot.register_next_step_handler(msg, proverka_ya)

	if call.data == 'промоактивация':
		msg = bot.send_message(call.message.chat.id,f"<b>ℹ️ Отправьте промокод:</b>", reply_markup=keyboards.main, parse_mode='HTML')
		bot.register_next_step_handler(msg, aktivpromo)


	if call.data[:12] == 'бткчек':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id,f'''👉 Для пополнения баланса <a href="https://t.me/BTC_CHANGE_BOT?start=13Rc4">BTC</a>|<a href="https://t.me/ETH_CHANGE_BOT?start=13Rc4">ETH</a>|<a href="https://t.me/LTC_CHANGE_BOT?start=13Rc4">LTC</a> Чеком просто отправьте боту ЧЕК в личные сообщения.

⏱ Наша система автоматически проверит чек, время займет до 1 минуты
''',reply_markup=keyboards.otmena, parse_mode='HTML',disable_web_page_preview = True)
		bot.register_next_step_handler(msg, btc_oplata_1)



	elif call.data == 'create_sdelka':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.from_user.id,  '''ℹ️ Вы создаёте сделку как продавец.

💳 Введите сумму сделки:''', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, create_sdelka)

	elif call.data == 'invite_sdelka':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.from_user.id,  '🔰 Укажите id сделки', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, invite_sdelka)


	elif call.data[:11] == 'pay_sdelka_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT summa FROM sdelki where id = '{call.data[11:]}'")
		summa = q.fetchone()
		q.execute(f"SELECT user_create FROM sdelki where id = '{call.data[11:]}'")
		user_create = q.fetchone()
		q.execute("SELECT balans FROM ugc_users where id = "+ str(call.from_user.id))
		bal_us = q.fetchone()
		if int(bal_us[0]) >= int(summa[0]):
			q.execute("update ugc_users set balans = balans - " + str(summa[0])+" where id = " +str(call.from_user.id))
			connection.commit()
			q.execute(f"update sdelki set oplata = 'Да' where id = '{call.data[11:]}'")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='✔️ Товар получил ',callback_data=f'sdelka_good_{call.data[11:]}'))
			bot.send_message(call.from_user.id,  f'''📜 Сделка: #{call.data[11:]} оплачена.

ℹ️ Напишите: {user_create[0]} что бы получить товар !''', reply_markup=keyboard)
			bot.send_message(user_create[0], f'''📜 Сделка: #G{call.data[11:]} оплачена.

ℹ️ Можете отправить товар покупателю: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> !''',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(call.from_user.id, 'Пополните баланс!', reply_markup=keyboards.main)


	elif call.data[:14] == 'otmena_sdelka_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		id_sdelka = call.data[14:]
		print(id_sdelka)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT user_create FROM sdelki where id = '{id_sdelka}'")
		user_create = q.fetchone()
		q.execute(f"SELECT user_invite FROM sdelki where id = '{id_sdelka}'")
		user_invite = q.fetchone()
		q.execute(f"update sdelki set status = 'Закрыта' where id = '{id_sdelka}'")
		connection.commit()
		q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
		uv_sdelki = q.fetchone()[0]
		bot.send_message(call.from_user.id,  f''''📜 Сделка: #{id_sdelka} отменена ! ''',parse_mode='HTML', reply_markup=keyboards.main)
		bot.send_message(user_create[0], f'''📜 Сделка: #{id_sdelka} отменена ! ''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:10] == 'otziv_yes_':
		global id_sdelka1
		id_sdelka1 = call.data[10:]
		print(id_sdelka1)
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.from_user.id,  'ℹ️ Напишите текст отзыва:', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, otziv_yes)

	elif call.data[:9] == 'otziv_no_':
		id_sdelka = call.data[9:]
		print(id_sdelka)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT user_create FROM sdelki where id = '{id_sdelka}'")
		user_create = q.fetchone()
		q.execute(f"SELECT user_invite FROM sdelki where id = '{id_sdelka}'")
		user_invite = q.fetchone()
		if float(user_create[0]) == int(call.from_user.id):
			print('popal v user_create')
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='👍',callback_data=f'user_plus_{user_invite[0]}'),types.InlineKeyboardButton(text='👎',callback_data=f'user_minus_{user_invite[0]}'))
			bot.send_message(call.from_user.id,  'ℹ️ Оцените работу id юзера', reply_markup=keyboard)
		else:
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='👍',callback_data=f'user_plus_{user_create[0]}'),types.InlineKeyboardButton(text='👎',callback_data=f'user_minus_{user_create[0]}'))
			bot.send_message(call.from_user.id,  'ℹ️ Оцените работу id юзера', reply_markup=keyboard)

	elif call.data[:10] == "user_plus_":
		otziv_id = call.data[10:]
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT name FROM ugc_users where id = '{otziv_id}'")
		iduser_sellname = q.fetchone()[0]
		q.execute("update ugc_users set raiting = raiting + " + str('1')+" where id = " +str(otziv_id))
		connection.commit()
		bot.send_message(call.message.chat.id, f'''<b>❤️ Спасибо за оценку, рейтинг @{iduser_sellname} будет повышен !</b>''',parse_mode='HTML')
		bot.send_message(otziv_id, f'''<b>👤 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> повысил вам рейтинг !</b>''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:8] == "otzivyes":
		global awfawfawaaa
		awfawfawaaa = call.data[8:]
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, 'Введите текст отзыва:',reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, otziv_2_2)

	elif call.data[:11] == "user_minus_":
		otziv_id = call.data[11:]
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT name FROM ugc_users where id = '{otziv_id}'")
		iduser_sellname = q.fetchone()[0]
		q = connection.cursor()
		q.execute("update ugc_users set raiting = raiting - " + str('2')+" where id = " +str(otziv_id))
		connection.commit()
		bot.send_message(call.message.chat.id, f'''<b>❤️ Спасибо за оценку, рейтинг @{iduser_sellname} будет понижен !</b>''',parse_mode='HTML')
		bot.send_message(otziv_id, f'''<b>👤 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> понизил вам рейтинг !</b>''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data == "awhat_wind":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='🥝 QIWI',callback_data=f'QIWI'),types.InlineKeyboardButton(text='💳 CARD',callback_data=f'CARD'))
		keyboard.add(types.InlineKeyboardButton(text='💱 BTC|ETH|LTC',callback_data=f'BTC'),types.InlineKeyboardButton(text='ЮMoney',callback_data=f'WMZ'))
		bot.send_message(call.message.chat.id, "<b>📤 Выберите платежную систему:</b>",parse_mode='HTML', reply_markup=keyboard)

	elif call.data == "QIWI":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>📤 Введите ваш Qiwi Кошелек (Без +):</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, qiwi_viplata)

	elif call.data == "CARD":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>📤 Введите ваш номер карты: (Visa или Mastercard)</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, card_viplata)

	elif call.data == "BTC":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, 'Введите сумму для выплаты', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, summa_vilata_btc)

	elif call.data == "WMZ":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>📤 Введите ваш Yandex:</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, yo_viplata)


	elif call.data == "vau":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='📝Создать',callback_data=f'vau_add'),types.InlineKeyboardButton(text='📨Активировать',callback_data=f'vau_good'))
		bot.send_message(call.message.chat.id, "<b>Что вы бы хотели сделать?</b>",parse_mode='HTML', reply_markup=keyboard)

	elif call.data == "vau_add":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT balans FROM ugc_users where id is " + str(call.message.chat.id))
		balanss = q.fetchone()
		msg = bot.send_message(call.message.chat.id, f'''На какую сумму RUB выписать Ваучер ? (Его сможет обналичить любой пользователь, знающий код).

Доступно: {balanss[0]} RUB''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vau_add)

	elif call.data == "vau_good":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '''Для активации ваучера отправьте его код:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vau_good)


	elif call.data[:13]  == "Открытьсделку":
		global iduser_sell
		iduser_sell = call.data[13:]
		msg = bot.send_message(call.message.chat.id, "<b>Введите сумму сделки в RUB:</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, create_sdelka1)

	elif call.data[:14]  == "отзывысмотреть":
		global id_otzivs
		global sasfasfasf
		sasfasfasf = call.data[14:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM otziv where user = '{sasfasfasf}' and id_otziv = 1")
		Winners = q.fetchall()
		for i in Winners:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🔄 Смотреть еще',callback_data=f'смотретьещеотзыв{2}'))
			bot.send_message(call.from_user.id, f'Отзыв от {i[3]} : <code>{i[2]}</code>' ,parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:16]  == "смотретьещеотзыв":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		id_otzivs = call.data[16:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		print(sasfasfasf)
		print(id_otzivs)
		q.execute(f"SELECT * FROM otziv where user = '{sasfasfasf}' and id_otziv = {id_otzivs}")
		Winners = q.fetchall()
		for i in Winners:
			id_otzivs = int(id_otzivs) + 1
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🔄 Смотреть еще',callback_data=f'смотретьещеотзыв{id_otzivs}'))

			bot.send_message(call.from_user.id, f'Отзыв от {i[3]} : <code>{i[2]}</code>' ,parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:11]  == "подтвердить":
		idsdelkas = call.data[11:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		try:
			status = q.execute(f'SELECT status FROM sdelki where id = "{idsdelkas}"').fetchone()[0]
			if str(status) == str('Открыта'):
				pokupatel = q.execute(f'SELECT user_create FROM sdelki where id = "{idsdelkas}"').fetchone()[0]
				summa = q.execute(f'SELECT summa FROM sdelki where id = "{idsdelkas}"').fetchone()[0]
				balance = summa
				curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
				summarub = float(balance)*float(curse)
				q.execute(f"update sdelki set status = 'Ожидает оплаты' where id = '{idsdelkas}'")
				connection.commit()
				q.execute(f"update sdelki set user_invite = '{call.message.chat.id}' where id = '{idsdelkas}'")
				connection.commit()
				q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{pokupatel}'")
				idubuyname = q.fetchone()[0]
				info = q.execute(f'SELECT info FROM sdelki where id = "{idsdelkas}"').fetchone()[0]

				bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{idsdelkas}

		➖ Покупатель: @{idubuyname}

		➖ Продавец: @{iduser_sellname}

		💰 Сумма: <code>{summa}</code> RUB

		📝 Условия: <code>{info}</code>

		♻️ Статус: Ожидайте уведомления об оплате''',parse_mode='HTML')
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Оплатить',callback_data=f'оплатитьсделку{idsdelkas}'))
				keyboard.add(types.InlineKeyboardButton(text='Отменить',callback_data=f'отказсделка{idsdelkas}'))
				bot.send_message(pokupatel, f'''🔰 Сделка: #G{idsdelkas}

		➖ Покупатель: @{idubuyname}

		➖ Продавец: @{iduser_sellname}

		💰 Сумма: <code>{summa}</code> RUB

		📝 Условия: <code>{info}</code>

		♻️ Статус: Ожидание оплаты''',parse_mode='HTML', reply_markup=keyboard)
		except:
			print('ss')
		

	
	elif call.data == 'fereralka':
		#bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT ref_colvo FROM ugc_users where id = " + str(call.from_user.id))
		ref_colvoo = q.fetchone()
		bot.send_message(call.from_user.id,  f'''<b>👥 Партнерская программа

▫️Что это?
Наша уникальная партнерская программа система позволит вам заработать крупную сумму без вложений. Вам необходимо лишь приглашать друзей и вы будете получать пожизненно 2% от их депозитов в боте.

📯 Ваша партнерская ссылка:</b>

https://t.me/SAVEGARANT_bot?start={call.from_user.id}

<b>👥 Всего рефералов:</b> {ref_colvoo[0]}''', parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)
	elif call.data[:16]  == "условиявыполнены":
		saasasasss = call.data[16:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{saasasasss}"').fetchone()[0]
		if str(status) == str('Оплачена'):
			user_create = q.execute(f'SELECT user_create FROM sdelki where id = "{saasasasss}"').fetchone()[0]
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{saasasasss}"').fetchone()[0]
			balance = summa
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			q.execute(f"update sdelki set status = 'Финал' where id = '{saasasasss}'")
			connection.commit()
			info = q.execute(f'SELECT info FROM sdelki where id = "{saasasasss}"').fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{user_create}'")
			idubuyname = q.fetchone()[0]
			saassaddd = types.InlineKeyboardMarkup()
			saassaddd.add(types.InlineKeyboardButton(text='Открыть арбитраж',callback_data=f'арбитраж{saasasasss}'))
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Отправить деньги продавцу',callback_data=f'отправитьбабкипродавцу{saasasasss}'))
			keyboard.add(types.InlineKeyboardButton(text='Открыть арбитраж',callback_data=f'арбитраж{saasasasss}'))
			bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{saasasasss}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Закрыта, ожидайте подтверждения от покупателя
''',parse_mode='HTML', reply_markup=saassaddd)

			bot.send_message(user_create, f'''🔰 Сделка: #G{saasasasss}

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{summa}</code> RUB

📝 Условия: <code>{info}</code>

♻️ Статус: Условия выполнены''',parse_mode='HTML', reply_markup=keyboard)



	elif call.data[:22]  == "отправитьбабкипродавцу":
		idsdelkasaaassaa = call.data[22:]
		
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{idsdelkasaaassaa}"').fetchone()[0]
		if str(status) == str('Оплачена'):
			info = q.execute(f'SELECT info FROM sdelki where id = "{idsdelkasaaassaa}"').fetchone()[0]
			user_invite = q.execute(f'SELECT user_invite FROM sdelki where id = "{idsdelkasaaassaa}"').fetchone()[0]
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{idsdelkasaaassaa}"').fetchone()[0]
			balance = summa
			q.execute("SELECT com_sdelka FROM config  where id = "+str(1))
			com_sdelka = q.fetchone()[0]
			ref_prozent = com_sdelka
			add_ref_money = float(summa)/100*float(ref_prozent)
			balance_add = float(summa) - float(add_ref_money)
			q.execute("update ugc_users set balans = balans + "+str(balance_add)+" where id = " + str(user_invite))
			connection.commit()
			q.execute(f"update sdelki set status = 'Закрыта' where id = '{idsdelkasaaassaa}'")
			connection.commit()
			q.execute("update ugc_users set sdelka_summa = sdelka_summa + " + str(summa)+" where id = " +str(call.message.chat.id))
			connection.commit()
			q.execute("update ugc_users set sdelka_summa = sdelka_summa + " + str(summa)+" where id = " +str(user_invite))
			connection.commit()
			q.execute("update ugc_users set sdelka_colvo = sdelka_colvo + " + str('1')+" where id = " +str(call.message.chat.id))
			connection.commit()
			q.execute("update ugc_users set sdelka_colvo = sdelka_colvo + " + str('1')+" where id = " +str(user_invite))
			connection.commit()
			q.execute(f"SELECT name FROM ugc_users where id = '{user_invite}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
			idubuyname = q.fetchone()[0]
			keyboardotziv = types.InlineKeyboardMarkup()
			keyboardotziv.add(types.InlineKeyboardButton(text='➕ Да',callback_data=f'otzivyes{user_invite}'))
			iduser_sellname = iduser_sellname
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='👍',callback_data=f'user_plus_{call.message.chat.id}'),types.InlineKeyboardButton(text='👎',callback_data=f'user_minus_{call.message.chat.id}'))
			keyboardaa = types.InlineKeyboardMarkup()
			keyboardaa.add(types.InlineKeyboardButton(text='👍',callback_data=f'user_plus_{user_invite}'),types.InlineKeyboardButton(text='👎',callback_data=f'user_minus_{user_invite}'))
			q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
			uv_sdelki = q.fetchone()[0]
			global id_sdelka_otziv
			global summa_sdelka_otziv
			id_sdelka_otziv = idsdelkasaaassaa
			summa_sdelka_otziv = summa
			q = q.execute('SELECT chat_user FROM ugc_users WHERE id IS '+str(call.message.chat.id))
			row = q.fetchone()
			if row != None:
				bot.send_message(row[0], f'''🔰 Сделка: #G{idsdelkasaaassaa} закрыта!
От @{iduser_sellname} для @{idubuyname}
💰 Сумма сделки: <code>{summa}</code> RUB
''',parse_mode='HTML')
				admin_chat = q.execute(f'SELECT user FROM chat_garant where chat_id = "{row[0]}"').fetchone()[0]
				ref_prozent = 95.5
				add_ref_money = float(summa)/100*float(ref_prozent)
				sum_vivod = float(summa) - float(add_ref_money)
				print(sum_vivod)
				q.execute("update ugc_users set balans = balans + "+str(sum_vivod)+" where id = " + str(admin_chat))
				connection.commit()
				bot.send_message(admin_chat, f'''🔰 Сделка: #G{idsdelkasaaassaa} Поступила комиссия <code>{sum_vivod}</code> RUB''',parse_mode='HTML')



			bot.send_message(uv_sdelki, f'''🔰 Сделка: #G{idsdelkasaaassaa} закрыта!
От @{iduser_sellname} для @{idubuyname}
💰 Сумма сделки: <code>{summa}</code> RUB
''',parse_mode='HTML')
			bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{idsdelkasaaassaa} закрыта!''',parse_mode='HTML', reply_markup=keyboards.main)
			users_id_otziv = user_invite
			bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{idsdelkasaaassaa}

Хотите оставить отзыв о @{iduser_sellname} ?

''',parse_mode='HTML', reply_markup=keyboardotziv)
			bot.send_message(user_invite, f'''🔰 Сделка: #G{idsdelkasaaassaa} закрыта!
Вам начислено <code>{summa}</code> RUB!
''',parse_mode='HTML', reply_markup=keyboards.main)
			bot.send_message(call.message.chat.id, f'''ℹ️ Оцените работу @{iduser_sellname}''',parse_mode='HTML', reply_markup=keyboardaa)
			bot.send_message(user_invite, f'''ℹ️ Оцените работу @{idubuyname}''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:11]  == "отказсделка":
		idsdelkasaaaotkaz = call.data[11:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		user_create = q.execute(f'SELECT user_create FROM sdelki where id = "{idsdelkasaaaotkaz}"').fetchone()[0]
		user_invite = q.execute(f'SELECT user_invite FROM sdelki where id = "{idsdelkasaaaotkaz}"').fetchone()[0]
		q.execute(f"DELETE FROM sdelki WHERE id = '{idsdelkasaaaotkaz}'")
		connection.commit()
		uv_sdelki = q.execute("SELECT uv_sdelki FROM config  where id = "+str(1)).fetchone()[0]
		bot.send_message(user_create, f'''🔰 Сделка: #G{idsdelkasaaaotkaz} Отменена''',parse_mode='HTML', reply_markup=keyboards.main)
		bot.send_message(user_invite, f'''🔰 Сделка: #G{idsdelkasaaaotkaz} Отменена''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:8]  == "арбитраж":
		arbitra = call.data[8:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{arbitra}"').fetchone()[0]
		if str(status) == str('Оплачена'):
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Да',callback_data=f'арбитда{arbitra}'))
			bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{arbitra} вы подтверждаете открытия арбитража ?''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:7]  == "арбитда":
		arbitras = call.data[7:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{arbitras}"').fetchone()[0]
		if str(status) == str('Оплачена'):
			info = q.execute(f'SELECT info FROM sdelki where id = "{arbitras}"').fetchone()[0]
			user_invite = q.execute(f'SELECT user_invite FROM sdelki where id = "{arbitras}"').fetchone()[0]
			user_create = q.execute(f'SELECT user_create FROM sdelki where id = "{arbitras}"').fetchone()[0]
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{arbitras}"').fetchone()[0]
			balance = summa
			q.execute(f"update sdelki set status = 'Арбитраж' where id = '{arbitras}'")
			connection.commit()
			q.execute(f"SELECT name FROM ugc_users where id = '{user_invite}'")
			iduser_sellname = q.fetchone()[0]
			idubuyname = q.execute(f"SELECT name FROM ugc_users where id = '{user_create}'").fetchone()[0]
			uv_arb = q.execute("SELECT uv_arb FROM config  where id = "+str(1)).fetchone()[0]

# 			bot.send_message(uv_arb, f'''🔰 Сделка: #G{arbitras} от @{idubuyname} для @{iduser_sellname}

# 💰 Сумма сделки: <code>{summa}</code> RUB

# ♻️ Статус: Арбитраж
# ''',parse_mode='HTML')

			bot.send_message(user_create, f'''🔰 Сделка: #G{arbitras} от @{idubuyname} для @{iduser_sellname}

💰 Сумма сделки: <code>{summa}</code> RUB

♻️ Статус: Арбитраж
	''',parse_mode='HTML', reply_markup=keyboards.main)
			bot.send_message(user_invite, f'''🔰 Сделка: #G{arbitras} от @{idubuyname} для @{iduser_sellname}

💰 Сумма сделки: <code>{summa}</code> RUB

♻️ Статус: Арбитраж
	''',parse_mode='HTML', reply_markup=keyboards.main)






	elif call.data[:14]  == "возвратсредств":
		idsdelkasaaa = call.data[14:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		status = q.execute(f'SELECT status FROM sdelki where id = "{idsdelkasaaa}"').fetchone()[0]
		if str(status) == str('Оплачена'):
			user_create = q.execute(f'SELECT user_create FROM sdelki where id = "{idsdelkasaaa}"').fetchone()[0]
			info = q.execute(f'SELECT info FROM sdelki where id = "{idsdelkasaaa}"').fetchone()[0]
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{idsdelkasaaa}"').fetchone()[0]
			balance = summa
			q.execute("update ugc_users set balans = balans + "+str(summa)+" where id = " + str(user_create))
			connection.commit()
			q.execute(f"update sdelki set status = 'Отменена' where id = '{idsdelkasaaa}'")
			connection.commit()
			q.execute(f"SELECT name FROM ugc_users where id = '{call.message.chat.id}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{user_create}'")
			idubuyname = q.fetchone()[0]
			q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
			uv_sdelki = q.fetchone()[0]
			bot.send_message(uv_sdelki, f'''🔰 Сделка: #G{idsdelkasaaa} отменена!
От @{idubuyname} для @{iduser_sellname}
💰 Сумма сделки: {summa} RUB''',parse_mode='HTML')
			bot.send_message(call.message.chat.id, f'''❌ Сделка: #G{idsdelkasaaa} от @{idubuyname} для @{iduser_sellname}  отменена !''',parse_mode='HTML', reply_markup=keyboards.main)
			bot.send_message(user_create, f'''❌ Сделка: #G{idsdelkasaaa} от @{idubuyname} для @{iduser_sellname}  отменена и {summa} RUB вернулись на баланс !''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:14]  == "просмотр сделки":
		prosmotridsdelka = call.data[14:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM sdelki where id = '{prosmotridsdelka}'")
		info = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		for i in info:
			if str(i[5]) == str('Арбитраж'):
				summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
				balance = i[6]
				curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
				summarub = float(balance)*float(curse)
				q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
				idubuyname = q.fetchone()[0]
				keyboard = types.InlineKeyboardMarkup()
				q.execute("SELECT url_ard FROM config  where id = "+str(1))
				url_ard = q.fetchone()[0]
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Написать арбитру',url=url_ard))
				bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]} от @{idubuyname} для @{iduser_sellname}

💰 Сумма сделки: <code>{i[6]}</code> RUB

♻️ Статус: Арбитраж''',parse_mode='HTML', reply_markup=keyboards.main)


			if str(i[5]) == str('Оплачена'):
				if int(i[1]) == int(call.message.chat.id):
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					balance = i[6]
					curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
					summarub = float(balance)*float(curse)
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
					ssssss = types.InlineKeyboardMarkup()
					ssssss.add(types.InlineKeyboardButton(text='Отправить деньги продавцу',callback_data=f'отправитьбабкипродавцу{i[0]}'))
					ssssss.add(types.InlineKeyboardButton(text='Открыть арбитраж',callback_data=f'арбитраж{i[0]}'))

					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]} от @{idubuyname}

💰 Сумма сделки: <code>{summa}</code> RUB''',parse_mode='HTML', reply_markup=ssssss)
				else:
					q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
					iduser_sellname = q.fetchone()[0]
					q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
					idubuyname = q.fetchone()[0]
					summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text='Открыть арбитраж',callback_data=f'арбитраж{i[0]}'))
					keyboard.add(types.InlineKeyboardButton(text='Возврат средств',callback_data=f'возвратсредств{i[0]}'))
					bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]} от @{idubuyname}

💰 Сумма сделки: <code>{summa}</code> RUB''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data[:14]  == "закрытые сделки":
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='🛃Как покупатель',callback_data=f'заксдел{1}'))
		keyboard.add(types.InlineKeyboardButton(text='🛂Как продавец',callback_data=f'заксдел{2}'))
		bot.send_message(call.message.chat.id, 'Выбери тип сделки', reply_markup=keyboard)

	elif call.data[:11]  == "закарбитраж":
		idsdelkazak = call.data[11:]
		wdawdawdaw = idsdelkazak.split('\n')[2]
		colvoaktiv = idsdelkazak.split('\n')[1]
		sumpromo = idsdelkazak.split('\n')[0]
		print(colvoaktiv)
		print(sumpromo)
		print(wdawdawdaw)
		if int(wdawdawdaw) == 1:
			sssaa = 'в пользу покупателя'
		else:
			sssaa = 'в пользу продавца'
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"update sdelki set status = 'Закрыта' where id = '{colvoaktiv}'")
		connection.commit()
		q.execute(f"SELECT * FROM sdelki where id = '{colvoaktiv}'")
		info = q.fetchall()
		for i in info:
			q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
			idubuyname = q.fetchone()[0]
			balance = i[6]
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
		q.execute("update ugc_users set balans = balans + "+str(i[6])+" where id = " + str(sumpromo))
		connection.commit()
		q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
		uv_sdelki = q.fetchone()[0]
		bot.send_message(i[1], f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Закрыта {sssaa} ''',parse_mode='HTML', reply_markup=keyboards.main)
		bot.send_message(i[2], f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Закрыта {sssaa}''',parse_mode='HTML', reply_markup=keyboards.main)


	elif call.data[:8]  == "aaadddd_":
		idarbysd = call.data[8:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM sdelki where id = '{idarbysd}'")
		info = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		
		for i in info:
			q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
			iduser_sellname = q.fetchone()[0]
			q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
			idubuyname = q.fetchone()[0]
			balance = i[6]
			curse = requests.get('https://blockchain.info/ticker').json()['RUB']['last']
			summarub = float(balance)*float(curse)
			summa = q.execute(f'SELECT summa FROM sdelki where id = "{i[0]}"').fetchone()[0]
		keyboard.add(types.InlineKeyboardButton(text='Закрыть в пользу покупателя',callback_data=f'закарбитраж{i[1]}\n{idarbysd}\n{1}'))
		keyboard.add(types.InlineKeyboardButton(text='Закрыть в пользу продавца',callback_data=f'закарбитраж{i[2]}\n{idarbysd}\n{2}'))

		bot.send_message(call.message.chat.id, f'''🔰 Сделка: #G{i[0]}.

➖ Покупатель: @{idubuyname}

➖ Продавец: @{iduser_sellname}

💰 Сумма: <code>{i[6]}</code> RUB

📝 Условия: <code>{i[7]}</code>

♻️ Статус: Арбитраж''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:14] == 'заблокировать_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT status FROM ugc_users where id = "+ str(call.data[14:]))
		roww = q.fetchone()[0]
		if roww == 'Активен':
			q.execute(f"update ugc_users set status = 'Заблокирован' where id = {call.data[14:]}")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Заблокирован")
		else:
			q.execute(f"update ugc_users set status = 'Активен' where id = {call.data[14:]}")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Разблокирован")

	elif call.data[:14]  == "арбитрыудалить":
		#awcawc == call.data[14:]
		msg = bot.send_message(call.message.chat.id, "Введите id", reply_markup = keyboards.otmena)
		bot.register_next_step_handler(msg,new_admin)

	elif call.data[:14]  == "схемаработы":
		bot.send_message(call.message.chat.id, '''📖Схема работы бота построена следующим образом:

1. ✅Покупатель пополняет свой счет в боте любым доступным и удобным для себя способом.
2. ✅Покупатель нажимает кнопку «открыть сделку».
3. ✅Покупателю высвечивается окно ввода юзернейма продавца для приглашения в сделку.
4. ✅После ввода юзернейма покупателю необходимо указать сумму сделки. Покупатель может прописать условия сделки, если они есть, или же выбрать сделку без обязательств.
5. ✅После подтверждения покупателем, продавцу приходит уведомление о новом этапе сделки, а покупатель может ожидать свой товар для последующей проверки.
6. ✅Если условия сделки соблюдены и покупателя устроил товар - необходмо отпустить средства.
7. ✅Продавцу приходит уведомление о успешном завершении сделки, после чего продавец имеет возможность вывести средства любым удобным способом.
🔁 Комиссия бота составляет: 7%.

🆘🛃В случае если покупатель хочет оспорить сделку, если условия не соответствуют оговоренными в сделке, либо же покупателя пытаются обмануть, ему необходимо нажать кнопку «открыть арбитраж», в таком случае модераторы SAVE CLICK отменят сделку в пользу покупателя в течении 10 минут с момента создания заявки.

❗️Внимание! Сделку должен начать Покупатель воспользовавшись поиском пользователей! Это важный момент.

🤗Удачи в сделках!''', reply_markup = keyboards.main)

	elif call.data[:14]  == "инфочат":
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='📓Схема работы бота',callback_data=f'схемаработы'))
		bot.send_message(call.message.chat.id, '''🤔Почему выгодно внедрять SAVE CLICK в свой чат?

📉😋😎При интеграции SAVE CLICK в чат действует пониженная комиссия на сделки, а именно -2% на сделки.

👯💰🤑При интеграции SAVE CLICK в чат владелец чата может зарабатывать на сделках проведенных в чате. Это значит владелец чата будет получать 0.5% от суммы сделки участников в чате пожизненно!


❓Как внедрять SAVE CLICK в чат и зарабатывать на сделках?

1️⃣ Владельцу чата необходимо перейти в меню интеграции в чат, нажав соответствующую кнопку в меню: «Интеграция в чат»

2️⃣ Далее нужно нажать кнопку «Добавить чат», далее добавьте бота в админы и укажите ID чата, узнать действующий ID чата можно в самом чате при добавлении бота, бот автоматически считает ID и выдаст правильный результат. Его копируете и вставляете в поле, в боте.

3️⃣ После добавления SAVE CLICK в чат выдайте админские права.

4️⃣ Готово! Теперь для того чтобы провести сделку внутри чата вам нужно прописать сделку в формате:
/garant @alexandrshcherbak 1000

5️⃣ В чат придет соответствующее оповещение.

6️⃣ Далее все происходит по стандартной схеме работы бота.''', reply_markup = keyboard)

	elif call.data[:14]  == "добавитьвчат":
		#awcawc == call.data[14:]
		msg = bot.send_message(call.message.chat.id, "ℹ️ Добавьте бота в чат и пришлите id которое отправит бот:", reply_markup = keyboards.otmena)
		bot.register_next_step_handler(msg,new_chat)

	elif call.data[:16]  == "изменитькоммисию":
		global comsa
		idedit = call.data[16:]
		if int(idedit) == 1:
			comsa = 'com_vvod'
		if int(idedit) == 2:
			comsa = 'com_vivod'
		if int(idedit) == 3:
			comsa = 'com_sdelka'
		msg = bot.send_message(call.message.chat.id, '''Отправьте новое значение:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, comsaedit)

	elif call.data[:13]  == "изменитьтекст":
		global idtexts
		idtext = call.data[13:]
		if int(idtext) == 1:
			idtexts = 'texts'
		if int(idtext) == 2:
			idtexts = 'timess'
		if int(idtext) == 3:
			idtexts = 'photo'
		msg = bot.send_message(call.message.chat.id, '''Отправьте новое значение:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, postedit)


	elif call.data[:20] == 'уведомлениянастройка':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT uv_dep FROM config  where id = "+str(1))
		uv_dep = q.fetchone()[0]
		q.execute("SELECT uv_arb FROM config  where id = "+str(1))
		uv_arb = q.fetchone()[0]
		q.execute("SELECT uv_sdelki FROM config  where id = "+str(1))
		uv_sdelki = q.fetchone()[0]
		q.execute("SELECT uv_vivod FROM config  where id = "+str(1))
		uv_vivod = q.fetchone()[0]
		q.execute("SELECT url_ard FROM config  where id = "+str(1))
		url_ard = q.fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='Изменить ид сделок',callback_data=f'edituv{1}'))
		keyboard.add(types.InlineKeyboardButton(text='Изменить ид арбитражей',callback_data=f'edituv{2}'))
		bot.send_message(call.message.chat.id, f'''id для уведомления:
Сделка(Новая/Закрыта):{uv_sdelki}
Сделка(Арбитраж): {uv_arb}
''',parse_mode='HTML', reply_markup=keyboard)
		
	elif call.data == 'изменитьтокен_':
		msg = bot.send_message(call.message.chat.id, 'Введи новый токен киви: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_token)

	elif call.data == 'изменитьномер_':
		msg = bot.send_message(call.message.chat.id, 'Введи новый номер: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_phone)

	elif call.data[:6] == 'edituv':
		global conf_uvs
		awfawfwa = call.data[6:]

		if int(awfawfwa) == 1:
			conf_uvs = 'uv_sdelki'
		if int(awfawfwa) == 2:
			conf_uvs = 'uv_arb'
		if int(awfawfwa) == 3:
			conf_uvs = 'uv_dep'
		if int(awfawfwa) == 4:
			conf_uvs = 'uv_vivod'
		if int(awfawfwa) == 5:
			conf_uvs = 'url_ard'

		msg = bot.send_message(call.message.chat.id, 'Введи новый id (Бот должен быть админом): ',parse_mode='HTML')
		bot.register_next_step_handler(msg, smena_id_uv)

	elif call.data[:15] == 'добавитьбаланс_':
		global id_user_edit_bal1
		id_user_edit_bal1 = call.data[15:]
		msg = bot.send_message(call.message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, add_money2)
			
	elif call.data[:17] == 'admin_search_user':
		msg = bot.send_message(call.message.chat.id, f'<b>Введи username пользователя\n(Вводить нужно без @)</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,searchuserss)

	elif call.data[:6] == 'vivod_':
		global id_user_viplata
		global idvivod
		idvivod = call.data[6:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM vivod where id = '{idvivod}'")
		row = q.fetchone()
		id_user_viplata = row[1]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='Подтвердить',callback_data=f'выводыыы1'))
		keyboard.add(types.InlineKeyboardButton(text='Отклонить',callback_data=f'выводыыы2'))
		bot.send_message(call.message.chat.id, f'''User: <code>{row[1]}</code>
Сумма с учетом комиссий: <code>{row[2]}</code>

Метод выплаты: <code>{row[3]}</code>

Реквизиты: <code>{row[5]}</code>
''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:8] == 'выводыыы':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		if int(call.data[8:]) == 1:
			q.execute(f"update vivod set status = 'off' where id = {idvivod}")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Отправить сообщение',callback_data=f'Отправитьсообщение'))
			bot.send_message(call.message.chat.id, f'''✔️ Выплата прошла''',parse_mode='HTML', reply_markup=keyboard)
			bot.send_message(id_user_viplata, f'''✔️ Выплата прошла''',parse_mode='HTML', reply_markup=keyboards.main)
		if int(call.data[8:]) == 2:
			q.execute(f"update vivod set status = 'off' where id = {idvivod}")
			connection.commit()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Отправить сообщение',callback_data=f'Отправитьсообщение'))
			bot.send_message(call.message.chat.id, f'''✖️ Выплата отклонена''',parse_mode='HTML', reply_markup=keyboard)
			bot.send_message(id_user_viplata, f'''✖️ Выплата отклонена''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data == 'Отправитьсообщение':
		msg= bot.send_message(call.message.chat.id, "<b>Введи текст</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, send_user)

	elif call.data == 'открытьсделкучат':
		pass


		
	elif call.data[:8] == 'Рассылка':
		global tipsend
		tipsend = call.data[8:]
		msg= bot.send_message(call.message.chat.id, "<b>Введи текст для рассылки</b>",parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, send_photoorno)
			
	elif call.data[:7]  == "заксдел":
		ctosdelka = call.data[7:]
		if int(ctosdelka) == 1:
			status = 'user_create'
		else:
			status = 'user_invite'
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM sdelki where {str(status)} = '{call.message.chat.id}'")
		info = q.fetchall()
		rand = random.randint(10000000,99999999999)
		keyboard = types.InlineKeyboardMarkup()
		for i in info:
			if str(i[5]) == str('Закрыта'):
				q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
				idubuyname = q.fetchone()[0]
				doc = open(f'G{rand}.txt', 'a', encoding='utf8')
				doc.write(f'''ID: #G{i[0]} | Покупатель: @{idubuyname} | Продавец: @{iduser_sellname} | Cумма: {i[6]} | Дата {i[3]} | Статус: {i[5]} \n''')
				doc.close()
				
			if str(i[5]) == str('Отменена'):
				q.execute(f"SELECT name FROM ugc_users where id = '{i[2]}'")
				iduser_sellname = q.fetchone()[0]
				q.execute(f"SELECT name FROM ugc_users where id = '{i[1]}'")
				idubuyname = q.fetchone()[0]
				doc = open(f'G{rand}.txt', 'a', encoding='utf8')
				doc.write(f'''ID: #G{i[0]} | Покупатель: @{idubuyname} | Продавец: @{iduser_sellname} | Cумма: {i[6]} | Дата {i[3]} | Статус: {i[5]} \n''')
				doc.close()
		try:
			file = open(f'G{rand}.txt', encoding='utf8')
			bot.send_document(call.message.chat.id,file, caption='Ваши сделки')
			file.close()
			os.remove(f'G{rand}.txt')
		except:
			bot.send_message(call.message.chat.id, 'Сделки отсутствуют', reply_markup=keyboards.main)

def aktivpromo(message):
    # Функция для активации промокода (заглушка)
    bot.send_message(message.chat.id, "Функция промокодов временно недоступна", reply_markup=keyboards.main)

def create_sdelka(message):
    # Функция создания сделки (заглушка)
    bot.send_message(message.chat.id, "Введите сумму сделки в RUB:", reply_markup=keyboards.otmena)
    # Здесь должна быть логика создания сделки

def invite_sdelka(message):
    # Функция приглашения в сделку (заглушка)
    bot.send_message(message.chat.id, "Введите ID сделки:", reply_markup=keyboards.otmena)
    # Здесь должна быть логика приглашения

def otziv_yes(message):
    # Функция отзыва (заглушка)
    global id_sdelka1
    bot.send_message(message.chat.id, "Напишите текст отзыва:", reply_markup=keyboards.otmena)		


bot.polling(True)
