import telebot
what_token = '1'
def get_token():
	bot_main = telebot.TeleBot('6439996870:AAEJHb4arn-D9r2pdjF-gAOuQUL8Q1Yq1po') #main
	bot_test = telebot.TeleBot('2143205965:AAEXdkG8nMQtobmUoeoNGQ38qXNgfZMPt_c') #test
	if what_token == '1':
		return bot_main
	else:
		return bot_test