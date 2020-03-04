from geopy.distance import geodesic
from viberbot.api.messages import URLMessage, RichMediaMessage
from viberbot.api.messages.text_message import TextMessage

from .utils import viber

mojka_1 = {'name': 'Мойка1', 'tel': '0677899999', 'lat': '47.812748', 'lon': '35.186212',
           'url': 'https://goo.gl/maps/VCpg6Ly9fNtV5HtX8'}
mojka_2 = {'name': 'Мойка2', 'tel': '0677899999', 'lat': '47.815788', 'lon': '35.182961',
           'url': 'https://developers.viber.com/docs/api/python-bot-api/#TextMessage'}
mojka_3 = {'name': 'Мойка3', 'tel': '0677899999', 'lat': '47.823787', 'lon': '35.167687',
           'url': 'https://pythonworld.ru/tipy-dannyx-v-python/slovari-dict-funkcii-i-metody-slovarej.html'}

list_location_mojki = [mojka_1, mojka_2, mojka_3]


def distance(lan_1, lon_1, lan_2, lon_2):
    newport_ri = (lan_1, lon_1)
    cleveland_oh = (lan_2, lon_2)
    return geodesic(newport_ri, cleveland_oh).km


def list_object(lat, lon, km, id):
    list_mojki = []

    for location in list_location_mojki:
        if distance(lat, lon, location['lat'], location['lon']) < km:
            list_mojki.append(location)

    if len(list_mojki) == 0:
        message = TextMessage(text='В вашем районе моек нет')
        viber.send_messages(id, [message])


    else:
        for element in list_mojki:
            SAMPLE_RICH_MEDIA = {
                "ButtonsGroupColumns": 6,
                "ButtonsGroupRows": 7,
                "BgColor": "#69C48A",
                "Buttons": [
                    {
                        "Columns": 6,
                        "Rows": 3,
                        "ActionType": "open-url",
                        "ActionBody": "https://www.google.com",
                        "Image": "http://html-test:8080/myweb/guy/assets/imageRMsmall2.png"
                    },
                    {
                        "Columns": 6,
                        "Rows": 2,
                        "Text": element['name'],
                        "ActionType": "open-url",
                        "ActionBody": "https://www.google.com",
                        "TextSize": "medium",
                        "TextVAlign": "middle",
                        "TextHAlign": "left"
                    },
                    {
                        "Columns": 6,
                        "Rows": 1,
                        "ActionType": "open-url",
                        "ActionBody": "tel:" + element['tel'],
                        "Text": "Позвонить",
                        "TextSize": "large",
                        "TextVAlign": "middle",
                        "TextHAlign": "middle",
                        "Image": "https://s14.postimg.org/4mmt4rw1t/Button.png"
                    },
                    {
                        "Columns": 6,
                        "Rows": 1,
                        "ActionType": "open-url",
                        "ActionBody": element['url'],
                        "Text": "Проложить маршрут",
                        "TextSize": "large",
                        "TextVAlign": "middle",
                        "TextHAlign": "middle"
                    }

                ]
            }

            message = RichMediaMessage(rich_media=SAMPLE_RICH_MEDIA, min_api_version=2)
            viber.send_messages(id, [message])
