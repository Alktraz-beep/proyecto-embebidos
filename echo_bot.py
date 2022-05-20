
import os
from gpiozero import LED
import telebot

bot=telebot.Telebot("5198248925:AAHSnTII8zvxnV7yA76RQziHT0DFNdGsGmw",parse_mode=None)
@bot.message_handler(commands=['/start','/help'])
def send_welcome(message):
    bot.reply_to(message,"Hola, que quieres pinche pendejo?");

@bot.message_handler(func=lambda message:true)
def echo_all(message):
    bot.reply_to(message,message.txt)



bot.infinity_polling()
