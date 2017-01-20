from telegram.ext import Updater
import csv
import datetime
import telegram


updater = Updater(token='321426391:AAEeOd-QaDt2CUKUruKYZzPGA8RT78IsrME')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="4-213 is the best room")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def add(bot,update,args):
	found = False
	scoresDict = []
	with open('scores.csv') as scoresFile:
		scoresReader = csv.DictReader(scoresFile,delimiter=';')
		for row in scoresReader:
			if row["Name"] == ''.join(args):
				row["Score"] = int(row["Score"])+1
				row["Who"] = update.message.from_user.first_name
				row["When"] = datetime.datetime.now().strftime("%d.%m %I:%M")
				found = True
			scoresDict.append(row)
	print(scoresDict)
	if found:
		fieldnames = ['Name', 'Score',"Who",'When']
		with open('scores.csv','w') as scoresFileW:
			writer = csv.DictWriter(scoresFileW,fieldnames=fieldnames,delimiter=';')
			writer.writeheader()
			for row in scoresDict:
				writer.writerow(row)
		bot.sendMessage(chat_id=update.message.chat_id, text="Added")
	else:
		bot.sendMessage(chat_id=update.message.chat_id, text="Not Found")

add_handler = CommandHandler('add', add, pass_args=True)
dispatcher.add_handler(add_handler)

def scores(bot,update):
	text = ''
	with open('scores.csv') as scoresFile:
		scoresReader = csv.DictReader(scoresFile,delimiter=';')
		for row in scoresReader:
			text+="_"+row["Name"]+"_ *"+row["Score"]+"* Updated: "
			text+=row["When"]+" by " +row["Who"]+"\n"
	bot.sendMessage(chat_id=update.message.chat_id, text=text,parse_mode=telegram.ParseMode.MARKDOWN)

scores_handler = CommandHandler('scores', scores)
dispatcher.add_handler(scores_handler)
	
updater.start_polling()