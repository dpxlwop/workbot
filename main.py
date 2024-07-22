import telebot
from telebot import types
from tk import get_token
from salary import get_salary_report


bot = get_token()
admins = [867992805]
need_help = []

id = []
name = []
with open('files/employee', 'r') as file:
    for line in file:
        try:
            line = line.rstrip('\n')
            id.append(int(line))
        except ValueError:
            line = line.rstrip('\n')
            name.append(line)
file.close()
employee = {id[a]: name[a] for a in range(0, len(id))}
print(f"{len(id)}'s loaded sucssesfully!")
print(employee)


@bot.message_handler(commands=["addme"])
def add_me_com(message):
    if message.from_user.id not in employee.keys():
        try:
            txt = 'Новый пользователь хочет присоедениться\nID: ' + str(message.from_user.id)
        except Exception as e:
            print(e)
        try:
            txt += '\nИмя: ' + str(message.from_user.first_name)
        except Exception as e:
            print(e)
        try:
            txt += '\nФамилия: ' + str(message.from_user.last_name)
        except Exception as e:
            print(e)
        txt += '\n\n Для добавления отправь: !add "user_id" "name_lastname"'
        bot.send_message(admins[0], txt)
        bot.send_message(message.from_user.id, 'Я отправил запрос администратору, пожалуйста, свяжись с ним - @dpxlwop')


@bot.message_handler(commands=["send2all"])
def send2all_com(message):
    if message.from_user.id in admins:
        counter = 0
        error_counter = 0
        for i in id:
            try:
                counter += 1
                bot.send_message(i, get_salary_report(i, employee, True))
                bot.send_message(i, 'Если зарплата, которую я отправил не сходится с зп, которая посчитана тобой - отпр'
                                    'авь @dpxlwop следующее:\n1.Пересланное сообщение от бота\n2.Скриншот/текстовый под'
                                    'счет отработанного тобой времени, где четко видно следующее:\n   -Дата\n   -Время '
                                    'начала смены\n   -Время конца смены\n   -Количество отработанных часов\n3. Напиши,'
                                    ' где конкретно и что не сходится')
                t2 = str(employee[i]) + ' ok'
                bot.send_message(admins[0], t2)
            except Exception as e:
                error_counter += 1
                print(e)
                t2 = str(employee[i]) + 'not ok\n' + 'error: ' + str(e)
                bot.send_message(admins[0], t2)
        bot.send_message(message.from_user.id, f'💰Отправка отчетов завершена!💰\n✅Успешно отправлено: {counter}✅\n❌Всего ошибок: {error_counter}❌')
    else:
        bot.send_message(message.from_user.id, 'у тебя нет прав :)')


@bot.message_handler(commands=["start"])
def start_com(message):
    if message.from_user.id in employee.keys():
        if message.from_user.id in admins:
            get_buttons(message, 1)
        else:
            get_buttons(message, 1)
    else:
        bot.send_message(message.from_user.id,
                         'Извини, сейчас у тебя нет доступа к этому боту, нажми сюда\n--> /addme <--\n что бы отправить'
                         ' заявку на вступление')


def get_buttons(message, menu_level):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    match menu_level:
        case 1:
            markup = types.ReplyKeyboardMarkup(row_width=1)
            emergency = types.KeyboardButton('🚨ЧП🚨')
            problem_client = types.KeyboardButton('Проблемный клиент🗣🤡')
            salary = types.KeyboardButton('Зарплата💸💰')
            #markup.add(emergency, problem_client, salary)
            markup.add(salary)
        case 2:
            emergency_cotton = types.KeyboardButton('ЧП КОТТОН🚨')
            emergency_hammer = types.KeyboardButton('ЧП ХАММЕР🚨')
            emergency_top_dancer = types.KeyboardButton('ЧП СКАМЕЙКА🚨')
            emergency_spinning = types.KeyboardButton('ЧП СПИННИНГ🚨')
            emergency_jump_around = types.KeyboardButton('ЧП ДЖАМП🚨')
            emergency_cosmo_jet = types.KeyboardButton('ЧП КОСМО🚨')
            menu_up = types.KeyboardButton('📱Главное меню📱')
            #markup.add(emergency_cotton, emergency_hammer, emergency_top_dancer, emergency_spinning,
            #           emergency_jump_around, emergency_cosmo_jet, menu_up)
        case 3:
            client_cotton = types.KeyboardButton('КЛИЕНТ КОТТОН🗣')
            client_hammer = types.KeyboardButton('КЛИЕНТ ХАММЕР🗣')
            client_top_dancer = types.KeyboardButton('КЛИЕНТ СКАМЕЙКА🗣')
            client_spinning = types.KeyboardButton('КЛИЕНТ СПИННИНГ🗣')
            client_jump_around = types.KeyboardButton('КЛИЕНТ ДЖАМП🗣')
            client_cosmo_jet = types.KeyboardButton('КЛИЕНТ КОСМО🗣')
            menu_up = types.KeyboardButton('📱Главное меню📱')
            #markup.add(client_cotton, client_hammer, client_top_dancer, client_spinning, client_jump_around,
            #           client_cosmo_jet, menu_up)
        case 4:
            salary_full = types.KeyboardButton('Полный отчет по дням💰📝')
            salary_short = types.KeyboardButton('Сводный отчет💰📈')
            send2all = types.KeyboardButton('Отправить полный отчет всем')
            if message.from_user.id in admins:
                markup.add(send2all)
            menu_up = types.KeyboardButton('📱Главное меню📱')
            markup.add(salary_short, salary_full, menu_up)
    bot.send_message(message.from_user.id, 'Выбери нужное действие:', reply_markup=markup)


@bot.message_handler(content_types='text')
def txt(message):
    match message.text:
        case '🚨ЧП🚨':
            get_buttons(message, 2)
        case 'Проблемный клиент🗣🤡':
            get_buttons(message, 3)
        case '📱Главное меню📱':
            get_buttons(message, 1)
        case 'Зарплата💸💰':
            get_buttons(message, 4)
        case 'Сводный отчет💰📈':
            bot.send_message(message.from_user.id, get_salary_report(message.from_user.id, employee, False))
            get_buttons(message, 1)
        case 'Полный отчет по дням💰📝':
            bot.send_message(message.from_user.id, get_salary_report(message.from_user.id, employee, True))
            get_buttons(message, 1)
        case _:
            mess = message.text.split()
            if mess[0] == 'ЧП':
                name = employee[message.from_user.id].split('_')
                ts = mess[0] + ' ' + mess[1] + '\nСообщение от: ' + name[0] + ' ' + name[1]
                for i in admins:
                    bot.send_message(i, ts)
                bot.send_message(message.from_user.id,
                                 'Хорошо, я отправил сообщение администратору.\n\nКратко напиши, что случилось, что бы '
                                 'я передал администратору')
                need_help.append(message.from_user.id)
            elif mess[0] == 'КЛИЕНТ':
                name = employee[message.from_user.id].split('_')
                ts = mess[0] + ' ' + mess[1] + '\nСообщение от: ' + name[0] + ' ' + name[1]
                for i in admins:
                    bot.send_message(i, ts)
                bot.send_message(message.from_user.id,
                                 'Хорошо, я отправил сообщение администратору, пожалуйста, подожди')
                get_buttons(message, 1)
            elif message.from_user.id in need_help:
                name = employee[message.from_user.id].split('_')
                ts = 'Дополнительное сообщение от: ' + name[0] + ' ' + name[1] + '\n' + message.text
                for i in admins:
                    bot.send_message(i, ts)
                bot.send_message(message.from_user.id, 'Отправлено! Администратор уже идет к тебе')
                need_help.remove(message.from_user.id)
                get_buttons(message, 1)
            elif message.from_user.id in admins:
                try:
                    if message.text == 'Отправить полный отчет всем':
                        markup = types.ReplyKeyboardMarkup(row_width=1)
                        ya_im_sure = types.KeyboardButton('Да, отправить полный отчет всем')
                        menu_up = types.KeyboardButton('📱Главное меню📱')
                        markup.add(ya_im_sure, menu_up)
                        bot.send_message(message.from_user.id, 'Ты уверен?', reply_markup=markup)
                    elif message.text == 'Да, отправить полный отчет всем':
                        send2all_com(message)
                    if mess[0] == '!add':
                        with open('files/employee', 'a') as f:
                            towrite = '\n' + mess[1 ] + '\n' + mess[2]
                            f.write(towrite)
                        employee[int(mess[1])] = mess[2]
                        bot.send_message(message.from_user.id, 'Пользователь ' + mess[2] + ' успешно добавлен!')
                        bot.send_message(int(mess[1]),
                                         'Администратор одобрил твою заявку на вступление, нажми сюда\n--> /start <--\n'
                                         'что бы начать пользоватсья ботом.')
                except Exception as e:
                    print('2', e)
            else:
                bot.reply_to(message, 'Этого я не умею😞😞')


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    if message.from_user.id == admins[0]:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'files/' + message.document.file_name
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, 'Сохранил!')
        except Exception as e:
            bot.reply_to(message, e)
    else:
        bot.reply_to(message, 'Этого я не умею😞😞')


if __name__ == '__main__':
    bot.infinity_polling()
