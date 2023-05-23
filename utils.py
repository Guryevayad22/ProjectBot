from requests import get  # библиотека запросов на сайты
from datetime import datetime, date  # библиотека для работы с датами и временем

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjRlNDZjYjU4MzRlNmE5OTQxM2YwYTU0OTJhYmQ2MGNjYjAzZjE1MTZjYzUzNmE2NjEzZDk1MmYxMGZjMWZjOWRlMjViMzNjMjg3YjY0ZmY1In0.eyJhdWQiOiJIdGp4UFRDX012NjZpOFYtb2JvRHV4Z05SM1VWTFhCQURfNkw3ZW9sMnZNIiwianRpIjoiNGU0NmNiNTgzNGU2YTk5NDEzZjBhNTQ5MmFiZDYwY2NiMDNmMTUxNmNjNTM2YTY2MTNkOTUyZjEwZmMxZmM5ZGUyNWIzM2MyODdiNjRmZjUiLCJpYXQiOjE2ODQ0OTU5NzUsIm5iZiI6MTY4NDQ5NTk3NSwiZXhwIjoxOTk5ODU1OTc1LjU1Mzg0OSwic3ViIjoiMTY0NSIsInNjb3BlIjpbImF1dGhlbnRpY2F0ZWQiLCJyZXN0X2FwaV9ib29raW5nX2J1c3kiXX0.j5fmTndMG5WbbJuPK7l923oARhjWf3XXTDnXEITVTHT1u-SZeIOWF7y3XHzNETFeoBystv6UdUKPTlvyUSmaI2svpk8QZ7Ld9xJ9_-LeDQHrcdU5TPaX5u57NnXx-TGPqdre7pH31m36Cs70btW7ptjoFDhkuYTZTFgpAaC8Ly3rTTxkB3wuz7YjsCl_8QxgAvWUZUqZGIHZZWkP9Vd0z6jWjI27YSSS5O3DzOY6i07yM00LthG7lVxDbQhIpUM8kPx6m9Ly7T8Xk_9siVYZPuusxLwuk43pQBAbKzPicFuc50yvORI-fIcYyRfhoclXK__7wAnzBpvh9Zz60Yxv9Q'


# timestamp - количество секунд с момента 1970-01-01 00:00:00, т.н. Epoch Time
def convert_timestamp_to_datetime(timestamp):  # переводит секунды в нормальную дату со временем
    return datetime.fromtimestamp(int(timestamp))


def convert_timestamp_to_date(timestamp):  # переводит секунды в нормальную дату
    return datetime.fromtimestamp(int(timestamp)).date()


def get_all_rooms():  # функция получения списка всех комнат
    url = 'https://physics.itmo.ru/ru[en]/rest/export/json/booking-resources?_format=json'
    headers = {
        'Authorization': f'Bearer {token}'  # заголовок для авторизации по токену
    }

    response = get(url, headers=headers).json()  # обращение к сервису и конвертация ответа в json формат
    # а поскольку это питон, будет создан объект типа словарь

    return response


def get_all_bookings():  # функция получения всех бронирований
    url = 'https://physics.itmo.ru/ru/rest/export/json/booking-busy?_format=json'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = get(url, headers=headers).json()

    # отбор бронирований, начало которых сегодня либо позже
    bookings = [book for book in response
                if convert_timestamp_to_date(book['booking_date_start'] >= date.today())]

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
    rooms = set()  # здесь должны быть переговорки
    # свободные переговорки = все переговорки - занятые переговорки
    # сеты здесь потому что так проще всего найти элементы, которые есть обоих множество
    return list(rooms - set(get_occupied_rooms(bookings)))


if __name__ == '__main__':
    r = get_all_rooms()
    print(r)
