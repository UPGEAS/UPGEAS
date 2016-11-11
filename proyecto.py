import atexit
import ConfigParser
import signal
import sys
import time
import th02
import PyBCM2835

import pyump_th02 as th02
import pyupm_grove as grove
import pyupm_grovespeaker as upmGrovespeaker
import pyupm_i2clcd as lcd

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

credentials = ConfigParser.ConfigParser()
credentialsfile = "credentials.config"
credentials.read(credentialsfile)

button = grove.GroveButton(8)
display = lcd.Jhd1313m1(0, 0x3E, 0x62)
light = grove.GroveLight(0)
relay = grove.GroveRelay(2)
humedad = th02.th02()

def functionLight(bot, update):
    luxes = light.value()
    bot.sendMessage(update.message.chat_id, text='Light! ' + str(luxes))

def functionMessage(bot, update):
    bot.sendMessage(update.message.chat_id, text=message + " " + message2)

def functionPicture(bot, update):
    bot.sendPhoto(update.message.chat_id, photo=open('documentation/image.jpg', 'rb'))

def functionRelay(bot, update):
    relay.on()
    time.sleep(2)
    relay.off()
    bot.sendMessage(update.message.chat_id, text='Relay!')

def functionEcho(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def SIGINTHandler(signum, frame):
	raise SystemExit

def exitHandler():
	print "Exiting"
	sys.exit(0)

atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)

if __name__ == '__main__':

    credential = credentials.get("telegram", "token")
    updater = Updater(credential)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("light", functionLight))
    dp.add_handler(CommandHandler("message", functionMessage))
    dp.add_handler(CommandHandler("picture", functionPicture))
    dp.add_handler(CommandHandler("relay", functionRelay))
    dp.add_handler(MessageHandler([Filters.text], functionEcho))

    updater.start_polling()

    message = "La humedad es "+ humedad
    message2 = "UPGEAS"

    while True:

        luxes = light.value()
        luxes = int(luxes)    
        display.setColor(luxes, luxes, luxes)
        display.clear()

        if button.value() is 1:
            display.setColor(255, 255, 0)
            display.setCursor(0,0)
            display.write(str(message))
            display.setCursor(1,0)
            display.write(str(message2))
            relay.on()
            time.sleep(1)
            relay.off()

        while button.value() is 1:
            display.scroll(True)
            time.sleep(.3)

    updater.idle()
