from requests import get  # библиотека запросов на сайты
from datetime import datetime, date  # библиотека для работы с датами и временем
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # используется для запуска функции check_bookings

# по расписанию

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImE0NTdmOWVlZGE0ZjBiYjFlMzVjZTNjNGJjZGM5ZWQxZWYyNGJlYjk0ZTc3NzMxMTE1YTQ1MDY0Zjk2OGExNzEzNjk3Yzk5OWE3MjIwY2IxIn0.eyJhdWQiOiJIdGp4UFRDX012NjZpOFYtb2JvRHV4Z05SM1VWTFhCQURfNkw3ZW9sMnZNIiwianRpIjoiYTQ1N2Y5ZWVkYTRmMGJiMWUzNWNlM2M0YmNkYzllZDFlZjI0YmViOTRlNzc3MzExMTVhNDUwNjRmOTY4YTE3MTM2OTdjOTk5YTcyMjBjYjEiLCJpYXQiOjE2ODQ4NjQwODQsIm5iZiI6MTY4NDg2NDA4NCwiZXhwIjoyMDAwMjI0MDg0LjEzODA4OSwic3ViIjoiMjA3NSIsInNjb3BlIjpbImF1dGhlbnRpY2F0ZWQiLCJyZXN0X2FwaV9ib29raW5nX2J1c3kiXX0.qtKnF49APsPFx6RKEP0f4IlNrKNUMLdIU7GLPNVVzaycPK8ZSVYE6g01ZQOIwUiP7qMkr0oBVhRuD0IPBhbnNOpZKWy0BXm87KVJ31U8kKWiDMSsuC4mSOvcmmTd8BDaryAaG4UsUC0BT3s3CaFH8U5DAxtgXyR5PkfcmJLajxJldYgN1dAWmm02Sf2fxoSPAYE3BcbKZDvW_8aDa4D-KCrE2L5zUWNrdcNsKFD81YZ2ApmDXr_mRPQnF7xnxQj65DvQuV1y3ypMp7m4Ix0YH-HIe2SwG3SFY6VmqLFJg2x7czBVAweGKuUsjx8G3KNzosWFm0U_mKsBCZYaU5JVfg'
all_rooms = []

bookings = []
map_name_id = {'Io': '2868',
               'Europa': '2869',
               'Ganymede': '2870',
               'Callisto': '2871',
               'Jupiter': '2872',
               '2536 (library)': '2873',
               'Ceres': '2876'}


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
            'Authorization': f'Bearer {token}'  # заголовок для авторизации по токену
        }

        response = get(url, headers=headers).json()
        # обращение к сервису и конвертация ответа в json формат
        # а поскольку это питон, будет создан объект типа словарь
        all_rooms = [book['name'] for book in response if book['parent_target_id'] == '2812']
    return all_rooms


def get_all_bookings():  # функция получения всех бронирований
    global bookings
    url = f'https://physics.itmo.ru/ru/rest/export/json/booking-busy' \
          f'?booking_date_start_value_op=>=&booking_date_start_value[value]={date.today()}' \
          f'&_format=json'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = get(url, headers=headers).json()

    # отбор бронирований _переговорок_ (второе условие), начало которых сегодня либо позже
    bookings = [book for book in response
                if convert_timestamp_to_date(book['booking_date_start']) >= date.today() and
                book['booking_equip'] in map_name_id.values()]
    return bookings


def get_occupied_rooms(bookings):  # получение занятых _в данный момент_ комнат
    rooms = []
    for booking in bookings:
        start_datetime = convert_timestamp_to_datetime(booking['booking_date_start'])
        end_datetime = convert_timestamp_to_datetime(booking['booking_date_end'])
        curr_datetime = datetime.now()
        if start_datetime <= curr_datetime <= end_datetime:
            rooms.append(booking['booking_equip'])

    return rooms


def get_free_rooms(bookings):  # функция получения свободных комнат
    rooms = set(get_all_rooms())
    # свободные переговорки = все переговорки - занятые переговорки
    # сеты здесь потому что так проще всего найти элементы, которые есть обоих множество
    return list(rooms - set(get_occupied_rooms(bookings)))


scheduler = AsyncIOScheduler()


# запуск обновления бронирований по расписанию каждые пять минут с момента запуска бота
async def on_startup(_):
    get_all_bookings()#кидает запрос сразу при запуске
    scheduler.add_job(get_all_bookings, 'interval', minutes=5)
