import requests
import config
import telebot
import datetime
import time
from bs4 import BeautifulSoup

from telebot import apihelper

apihelper.proxy = {'https': 'socks5://georgy.komarov:2naturala1613@aws.komarov.ml:7777'}

bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


wdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
wdays_rus = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def parse_schedule_for_day(web_page, _):
    soup = BeautifulSoup(web_page, "html5lib")

    _ = _[1:]

    num = wdays.index(_) + 1

    # Получаем таблицу с расписанием на указанный день недели
    schedule_table = soup.find("table", attrs={"id": "%dday" % (num)})

    if schedule_table == None:
        return None, None, None
    else:
        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
    
        return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    _, week, group = message.text.split()
    web_page = get_page(group, week)

    if _ == '/sunday':
        _ = '/monday'
        bot.send_message(message.chat.id, 'В воскресенье пар нет. Расписание на понедельник:', parse_mode='HTML')
        
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_day(web_page, _)
    if times_lst == locations_lst == lessons_lst == None:
        bot.send_message(message.chat.id, 'В этот день у указанной группы пар нет.', parse_mode='HTML')
    else:
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()

    ct = datetime.datetime.today()
    h = str(ct.hour)
    m = str(ct.minute)
    if ct.hour < 10:
        h = '0' + h
    if ct.minute < 10:
        m = '0' + m
    curtime = h + ':' + m

    week = datetime.date.today().isocalendar()[1] - 35
    week = week % 2 + 1

    web_page = get_page(group, week)
    resp = ''
    wday = '/' + wdays[datetime.date.today().weekday()]
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_day(web_page, wday)
    
    if times_lst == locations_lst == lessons_lst == None:
        pass
    else:
        for time in times_lst:
            if time > curtime:
                i = times_lst.index(time)
                time, location, lession = times_lst[i], locations_lst[i], lessons_lst[i]
                resp += 'Ближайшая пара сегодня:\n<b>{}</b>, {}, {}\n'.format(time, location, lession)
            if resp:
                break
    
    if resp == '':
        for d in range(1, 7):
            da = d
            if datetime.date.today().weekday() + d > 6:
                da = d - 7
                if week == 1:
                    web_page = get_page(group, week + 1)
                else:
                    web_page = get_page(group, week - 1)
            wday = '/' + wdays[datetime.date.today().weekday() + da]
            times_lst, locations_lst, lessons_lst = \
                parse_schedule_for_day(web_page, wday)
    
            if times_lst == locations_lst == lessons_lst == None:
                pass
            else:
                time, location, lession = times_lst[0], locations_lst[0], lessons_lst[0]
                resp += 'Ближайшая пара:\n<b>{}</b>\n<b>{}</b>, {}, {}\n'.format(wdays_rus[datetime.date.today().weekday() + da], time, location, lession)
            if resp:
                break
    bot.send_message(message.chat.id, resp, parse_mode='HTML')   


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    tom = datetime.date.today().weekday() + 1
    if tom == 7:
        wday = 'monday'
    else:
        wday = wdays[tom]
    resp = ''
    if wday == 'sunday':
        resp += 'Завтра воскресенье. Пар нет. Можно отдыхать!\n\nРасписание на понедельник:\n\n'
        wday = 'monday'
    week = datetime.date.today().isocalendar()[1] - 35
    if wday == 'monday':
        week = week + 1
    week = week % 2 + 1
    web_page = get_page(group, week)
    wday = '/' + wday
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_day(web_page, wday)
    if times_lst == locations_lst == lessons_lst == None:
        resp += 'Завтра у указанной группы пар нет.\n\n'
    else:
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, week, group = message.text.split()
    web_page = get_page(group, week)

    resp = ''
    for day in wdays:
        resp += "<b>{}:</b>\n".format(wdays_rus[wdays.index(day)])
        day = '/' + day
        times_lst, locations_lst, lessons_lst = \
            parse_schedule_for_day(web_page, day)
        if times_lst == locations_lst == lessons_lst == None:
            resp += 'В этот день у указанной группы пар нет.\n\n'
        else:
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)