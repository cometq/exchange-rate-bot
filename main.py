# Imports
import asyncio, requests
from bs4 import BeautifulSoup
import sys
from telebot.async_telebot import AsyncTeleBot, types


# Automatic exchange rate updater (web scrping)
async def periodic():
    global gbp, cad, eur, aud
    while True:
        soup = BeautifulSoup(requests.get('https://www.x-rates.com/').text, features="lxml")
        gbp = soup.find('a', href="https://www.x-rates.com/graph/?from=GBP&to=USD").text
        cad = soup.find('a', href="https://www.x-rates.com/graph/?from=CAD&to=USD").text
        eur = soup.find('a', href="https://www.x-rates.com/graph/?from=EUR&to=USD").text
        aud = soup.find('a', href="https://www.x-rates.com/graph/?from=AUD&to=USD").text
        await asyncio.sleep(30)

# Creating Async loop to launch task in a different thread
loop = asyncio.get_event_loop()
task = loop.create_task(periodic())

# Getting token from a extern file
try:
    with open('token.txt', 'r') as file:
        token = file.read().rstrip()
except Exception:
    print("Could not get bot token")
    sys.exit(0)

# Telegram bot methods
bot = AsyncTeleBot(token)
@bot.message_handler(commands=['start'])
async def send_hi(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("🚀 Get Exchange Rates")
    markup.add(item)
    await bot.send_message(message.chat.id, "👋 Hey! To get current USD exhcange rate click the button below", reply_markup=markup)

@bot.message_handler(content_types='text')
async def send_exchange(message):
    if message.text == "🚀 Get Exchange Rates":
        await bot.send_message(message.chat.id, f"🇺🇸 -> 🇬🇧: {gbp}\n🇺🇸 -> 🇨🇦: {cad}\n🇺🇸 -> 🇪🇺: {eur}\n🇺🇸 -> 🇦🇺: {aud}")

# Creating new thread to launch bot
task_bot = loop.create_task(bot.polling())

# Launching all asyncio process
try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass

