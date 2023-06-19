from requests import get  # библиотека запросов на сайты
from datetime import datetime, date  # библиотека для работы с датами и временем
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # используется для запуска функции check_bookings
# по расписанию
from config import access_token

all_rooms = []

bookings = []
map_name_id = {
    'Io': '2868',
    'Europa': '2869',
    'Ganymede': '2870',
    'Callisto': '2871',
    'Jupiter': '2872',
    '2536 (library)': '2873',
    'Ceres': '2876'
}

map_id_name = {
    '2868': 'Io',
    '2869': 'Europa',
    '2870': 'Ganymede',
    '2871': 'Callisto',
    '2872': 'Jupiter',
    '2873': '2536 (library)',
    '2876': 'Ceres'
}


# timestamp - количество секунд с момента 1970-01-01 00:00:00
def convert_timestamp_to_datetime(timestamp):  # переводит секунды в нормальную дату со временем
    return datetime.fromtimestamp(int(timestamp))


def convert_timestamp_to_date(timestamp):  # переводит секунды в нормальную дату
    return datetime.fromtimestamp(int(timestamp)).date()


def get_all_rooms():  # функция получения списка всех комнат
    global all_rooms
    if not all_rooms:
        url = 'https://physics.itmo.ru/ru/rest/export/json/booking-resources?_format=json'
        headers = {
            'Authorization': f'Bearer {access_token}'  # заголовок для авторизации по токену
        }

        response = get(url, headers=headers).json()
        # обращение к сервису и конвертация ответа в json формат
        # а поскольку это питон, будет создан объект типа словарь
        all_rooms = [room['name'] for room in response if room['parent_target_id'] == '2812']
        all_rooms.extend(
            [room['name'] for room in response if room['name'] in ('2530', '2531')]
        )

        all_rooms = sorted(all_rooms)
    return all_rooms


def get_all_bookings():  # функция получения всех бронирований
    global bookings
    url = f'https://physics.itmo.ru/ru/rest/export/json/booking-busy' \
          f'?booking_date_start_value_op=>=&booking_date_start_value[value]={date.today()}' \
          f'&_format=json'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = get(url, headers=headers).json()
    # отбор бронирований _переговорок_ (второе условие), начало которых сегодня либо позже
    bookings = [book for book in response
                if convert_timestamp_to_date(book['booking_date_start']) >= date.today() and
                book['booking_equip'] in map_name_id.values()]


def get_occupied_rooms(bookings, search_time=datetime.now()):  # получение занятых _в данный момент_ комнат
    rooms = []
    for booking in bookings:
        start_datetime = convert_timestamp_to_datetime(booking['booking_date_start'])
        end_datetime = convert_timestamp_to_datetime(booking['booking_date_end'])
        curr_datetime = search_time
        if start_datetime <= curr_datetime <= end_datetime:
            name = map_id_name[booking['booking_equip']]
            rooms.append(name)

    return sorted(set(rooms))


def get_free_rooms(bookings, search_time=datetime.now()):  # функция получения свободных комнат
    rooms = []
    for booking in bookings:
        start_datetime = convert_timestamp_to_datetime(booking['booking_date_start'])
        end_datetime = convert_timestamp_to_datetime(booking['booking_date_end'])
        curr_datetime = search_time
        if not start_datetime <= curr_datetime <= end_datetime:
            name = map_id_name[booking['booking_equip']]
            rooms.append(name)

    return sorted(set(rooms))


def get_bookings():
    return bookings


scheduler = AsyncIOScheduler()


# запуск обновления бронирований по расписанию каждые пять минут с момента запуска бота
async def on_startup(_):
    get_all_bookings()  # кидает запрос сразу при запуске
    scheduler.add_job(get_all_bookings, 'interval', minutes=5)


def test():
    url = f'https://physics.itmo.ru/ru/rest/export/json/booking-busy'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    print(get(url, headers=headers))
