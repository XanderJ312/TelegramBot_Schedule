import telebot
import json
from datetime import datetime, timedelta
import requests

TOKEN = 'telegram_bot_token'     # here must be token of your telegram bot.
                                 # This token you can take from official telegram bot - https://t.me/BotFather

admin = "admin_id"     #Admins id of group (int, not string)

bot = telebot.TeleBot(TOKEN)

def get_next_sunday(sunday):
    days_ahead = (6 - sunday.weekday() + 7) % 7
    next_sunday = sunday + timedelta(days=days_ahead)
    return next_sunday

def create_schedule(members, id_members):
    schedule = []
    sundays = []
    next_sunday = datetime.today()
    for i, member in enumerate(members):
        next_sunday = get_next_sunday(next_sunday)
        sundays.append(next_sunday)
        schedule_item = {
            "username": member,
            "id": id_members[i],
            "date": next_sunday.strftime("%d-%m-%Y"),
            "done": False
        }
        schedule.append(schedule_item)
        next_sunday += timedelta(weeks=1)

    return schedule


def readFile():
    with open('Schedules/Cleaning.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data

def write_file(schedule_json):
    with open('Schedules/Cleaning.json', 'w') as f:
        f.write(json.dumps(schedule_json))
        f.close()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Нахер пошел еще раз")


@bot.message_handler(commands=['generate'])
def generate_schedule(message):
    if (message.from_user.id == admin):
        schedule_data = readFile()
        members = schedule_data['members']*3
        id_members = schedule_data['id_members']*3
        schedule = create_schedule(members, id_members)
        new_schedule = {
            "name": schedule_data['name'],
            "members": schedule_data['members'],
            "id_members": schedule_data['id_members'],
            "dates": schedule
        }
        write_file(new_schedule)
        bot.send_message(message.chat.id, "New schedule was created!")


@bot.message_handler(commands=['show'])
def show_func(message):
    read_data = readFile()
    data_dates = list(read_data['dates'])
    dates = ""
    for date in data_dates:
        if(date['done']==True):
            status_emoji = "✅"
        else:
            status_emoji = "❌"
        dates = dates + str(status_emoji + " [" + date['date'] + "] - " + date['username'] + "\n")

    sent_message = bot.send_message(message.chat.id, "Name: " + str(read_data['name']) + "\n\n" + dates)

    url = f"https://api.telegram.org/bot{TOKEN}/unpinAllChatMessages?chat_id={message.chat.id}"
    response = requests.get(url)

    url = f"https://api.telegram.org/bot{TOKEN}/pinChatMessage?chat_id={message.chat.id}&message_id={sent_message.message_id}"
    response = requests.get(url)


@bot.message_handler(commands=['done'])
def done_check(message):
    read_data = readFile()
    data_dates = list(read_data['dates'])
    is_Exist = False

    current_date = datetime.today().date()
    date_formated = current_date.strftime("%d-%m-%Y")

    for date in data_dates:
        if (date['date'] == date_formated and date['id'] == str(message.from_user.id)):
            bot.send_message(message.chat.id, "Nice!")
            date['done'] = True
            write_file(read_data)
            is_Exist = True
            show_func(message)
            break

    if is_Exist == False:
        bot.send_message(message.chat.id, "There is no record listed for today with your name on it!")


bot.polling(none_stop=True)