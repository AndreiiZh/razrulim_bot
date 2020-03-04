import re
import urllib

from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from viberbot.api.messages import TextMessage, KeyboardMessage, ContactMessage, PictureMessage, URLMessage, \
    RichMediaMessage, LocationMessage, FileMessage
from viberbot.api.messages.data_types.contact import Contact
from viberbot.api.viber_requests import ViberUnsubscribedRequest, ViberSubscribedRequest, ViberMessageRequest, \
    ViberConversationStartedRequest
from viberbot.api.messages.data_types.location import Location

from .models import ViberUser
from .utils import viber
from .location import list_object


@csrf_exempt
def set_webhook(request):
    event_types = ["failed",
                   "subscribed",
                   "unsubscribed",
                   "conversation_started"]
    url = f'https://{settings.ALLOWED_HOSTS[0]}/viber/callback/'
    viber.set_webhook(url=url, webhook_events=event_types)
    return HttpResponse('Ok')


# @csrf_exempt
# def callback(request):
#     if request.method == 'POST':
#         viber_request = viber.parse_request(request.body)
#         print(viber_request)
#         viber.send_messages(
#             viber_request.sender.id,
#             TextMessage(text='Hi')
#         )
#         if isinstance(viber_request, ViberMessageRequest):
#             if isinstance(viber_request.message, TextMessage):
#                 print(viber_request.message)
#                 ViberUser.objects.update_or_create(viber_id=viber_request.user.id,
#                                                    name=viber_request.user.name,
#                                                    defaults={'is_active': True})
#                 viber.send_messages(viber_request.sender.id, [TextMessage(text='Это текст')])
#             elif isinstance(viber_request.message, PictureMessage):
#                 url_picture = viber_request.message.media
#                 urllib.request.urlretrieve(url_picture, 'viber_picture.jpg')
#                 print(url_picture)
#                 viber.send_messages(viber_request.sender.id, [TextMessage(text='Это картинка')])
#             elif isinstance(viber_request.message, ContactMessage):
#                 print(viber_request.message.contact.phone_number)
#                 viber.send_messages(viber_request.sender.id, [TextMessage(text='Спасибо за телефон')])
#                 ViberUser.objects.update_or_create(viber_id=viber_request.sender.id,
#                                                    defaults={
#                                                        'phone_number': viber_request.message.contact.phone_number})
#             print(viber_request)
#
#
#         elif isinstance(viber_request, ViberSubscribedRequest):
#             ViberUser.objects.update_or_create(viber_id=viber_request.user.id,
#                                                defaults={
#                                                    'is_active': True,
#                                                    'name': viber_request.user.name,
#                                                    'language': viber_request.user.language,
#                                                    'country': viber_request.user.country,
#                                                    'api_version': viber_request.user.api_version,
#                                                }
#                                                )
#
#             SAMPLE_KEYBOARD = {
#                 "Type": "keyboard",
#                 "Buttons": [
#                     {
#                         "Columns": 3,
#                         "Rows": 2,
#                         "BgColor": "#e6f5ff",
#                         "BgMedia": "http://link.to.button.image",
#                         "BgMediaType": "picture",
#                         "BgLoop": True,
#                         "ActionType": "share-phone",
#                         "ActionBody": "This will be sent to your bot in a callback",
#                         "ReplyType": "message",
#                         "Text": "Нажми меня!"
#                     }
#                 ]
#             }
#
#             viber.send_messages(viber_request.user.id,
#                                 [TextMessage(text='Hi'), KeyboardMessage(tracking_data='tracking_data',
#                                                                          keyboard=SAMPLE_KEYBOARD,
#                                                                          min_api_version=3)])
#
#         elif isinstance(viber_request, ViberUnsubscribedRequest):
#             ViberUser.objects.update_or_create(viber_id=viber_request.user_id, defaults={'is_active': False})
#
#         return HttpResponse(status=200)
#
#
# @csrf_exempt
# def send_message_for_user(request):
#     user = ViberUser.objects.get(id='GfgEPQmjGER68tg0+CkPDQ==')
#
#     SAMPLE_KEYBOARD = {
#         "Type": "keyboard",
#         "Buttons": [
#             {
#                 "Columns": 3,
#                 "Rows": 1,
#                 "BgColor": "#e6f5ff",
#                 "BgMedia": "http://link.to.button.image",
#                 "BgMediaType": "picture",
#                 "BgLoop": True,
#                 "ActionType": "share-phone",
#                 "ActionBody": "This will be sent to your bot in a callback",
#                 "ReplyType": "message",
#                 "Text": "push me"
#             }
#         ]
#     }
#
#     viber.send_messages(user.viber_id, [KeyboardMessage(tracking_data='tracking_data',
#                                                         keyboard=SAMPLE_KEYBOARD,
#                                                         min_api_version=3)])
#
#     return HttpResponse('Привет')

# **************************************************************

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        viber_request = viber.parse_request(request.body)

        if isinstance(viber_request, ViberConversationStartedRequest):
            viber.send_messages(viber_request.user.id, [
                TextMessage(text='Вас приветствует бот!')
            ])

        elif isinstance(viber_request, ViberSubscribedRequest):
            # user_detail = viber.get_user_details(viber_request.user.id)
            # ViberUser.objects.update_or_create(viber_id=viber_request.user.id,
            #                                    name=viber_request.user.name,
            #                                    language=viber_request.user.language,
            #                                    country=viber_request.user.country,
            #                                    api_version=viber_request.user.api_version,
            #                                    defaults={'is_active': True})
            viber.send_messages(viber_request.user.id, [
                TextMessage(text='Thanks')
            ])

        elif isinstance(viber_request, ViberMessageRequest):
            if isinstance(viber_request.message, TextMessage):
                ViberUser.objects.update_or_create(viber_id=viber_request.sender.id,
                                                   name=viber_request.sender.name,
                                                   language=viber_request.sender.language,
                                                   country=viber_request.sender.country,
                                                   api_version=viber_request.sender.api_version,
                                                   defaults={'is_active': True})
                keyboard_home = {
                    "Type": "keyboard",
                    "Buttons": [{
                        "Columns": 3,
                        "Rows": 1,
                        "Text": "Prezentacje",
                        "ActionType": "reply",
                        "ActionBody": "prezentacje",

                    },
                        {
                            "Columns": 3,
                            "Rows": 1,
                            "Text": "Wydarzenia",
                            "ActionType": "reply",
                            "ActionBody": "wydarzenia",
                        },
                        {
                            "Columns": 3,
                            "Rows": 1,
                            "Text": "Zmartwiony",
                            "ActionType": "reply",
                            "ActionBody": "zmartwiony",
                        },
                        {
                            "Columns": 3,
                            "Rows": 1,
                            "Text": "Uczyć się polskiego",
                            "ActionType": "reply",
                            "ActionBody": "uczyć się polskiego",
                        },
                        {
                            "Columns": 3,
                            "Rows": 1,
                            "Text": "Rozkład jazdy",
                            "ActionType": "reply",
                            "ActionBody": "rozkład jazdy",
                        },
                        {
                            "Columns": 3,
                            "Rows": 1,
                            "Text": "Jesteśmy",
                            "ActionType": "reply",
                            "ActionBody": "jesteśmy",
                        },
                    ]
                }

                # keyboard_home = {
                #     "Type": "keyboard",
                #     "Buttons": [{
                #         "Columns": 3,
                #         "Rows": 1,
                #         "Text": "locations",
                #         "ActionType": "location-picker",
                #         "ActionBody": "",
                #
                #     }]
                # }
                message = KeyboardMessage(tracking_data='tracking_data', keyboard=keyboard_home)
                viber.send_messages(viber_request.sender.id, [message])

                keyboard_exit = {
                    "Type": "keyboard",
                    "Buttons": [{
                        "Columns": 6,
                        "Rows": 1,
                        "Text": "Wróć",
                        "ActionType": "reply",
                        "ActionBody": "wróć",

                    }]
                }

                if str(viber_request.message.text) == 'prezentacje':
                    # keyboard_exit = {
                    #     "Type": "keyboard",
                    #     "Buttons": [{
                    #         "Columns": 6,
                    #         "Rows": 1,
                    #         "Text": "Wróć",
                    #         "ActionType": "reply",
                    #         "ActionBody": "wróć",
                    #
                    #     }]
                    # }
                    keyboard_message = KeyboardMessage(tracking_data='tracking_data', keyboard=keyboard_exit)
                    message = URLMessage(media="https://drive.google.com/open?id=1iirBXn0AXtddNkVv-OX5bwbzWwjErjYw")
                    viber.send_messages(viber_request.sender.id, [message, keyboard_message])

                elif str(viber_request.message.text) == 'wydarzenia':
                    keyboard_message = KeyboardMessage(tracking_data='tracking_data', keyboard=keyboard_exit)
                    message = PictureMessage(media='https://5fd86f1e.ngrok.io/media/marafon2.jpg',
                                             text="")
                    viber.send_messages(viber_request.sender.id, [message, keyboard_message])


            elif isinstance(viber_request.message, LocationMessage):
                location = str(viber_request.message.location)
                lat = re.search('(?:lat=)(.................)', location)
                lon = re.search('(?:lon=)(.................)', location)
                location_user = {'lat': '', 'lon': ''}

                if lat:
                    location_user['lat'] = lat[1]

                if lon:
                    location_user['lon'] = lon[1]

                list_object(location_user['lat'], location_user['lon'], 1, viber_request.sender.id)

    # if isinstance(viber_request, ViberMessageRequest):
    #     message = viber_request.message
    #     text = message.text
    #     text = text.split('|')
    #     text_type = text[0]
    #     text_message = ''
    #     SAMPLE_KEYBOARD = {
    #         "Type": "keyboard",
    #         "Buttons": [{
    #             "Columns": 2,
    #             "Rows": 2,
    #             "Text": "<br><font color=\"#494E67\"><b>ASIAN</b></font>",
    #             "TextSize": "large",
    #             "TextHAlign": "center",
    #             "TextVAlign": "middle",
    #             "ActionType": "reply",
    #             "ActionBody": "ASIAN",
    #             "BgColor": "#f7bb3f",
    #             "Image": "https://s18.postimg.org/9tncn0r85/sushi.png"
    #         }, {
    #             "Columns": 2,
    #             "Rows": 2,
    #             "Text": "<br><font color=\"#494E67\"><b>FRENCH</b></font>",
    #             "TextSize": "large",
    #             "TextHAlign": "center",
    #             "TextVAlign": "middle",
    #             "ActionType": "open-url",
    #             "ActionBody": "tel:+380966600745",
    #             "BgColor": "#7eceea",
    #             "Image": "https://s18.postimg.org/ntpef5syd/french.png"
    #         }, {
    #             "Columns": 2,
    #             "Rows": 2,
    #             "Text": "<br><font color=\"#494E67\"><b>MEXICAN</b></font>",
    #             "TextSize": "large",
    #             "TextHAlign": "center",
    #             "TextVAlign": "middle",
    #             "ActionType": "reply",
    #             "ActionBody": "Mexican",
    #             "BgColor": "#f6f7f9",
    #             "Image": "https://s18.postimg.org/t8y4g4kid/mexican.png"
    #         }, {
    #             "Columns": 2,
    #             "Rows": 2,
    #             "Text": "<br><font color=\"#494E67\"><b>ITALIAN</b></font>",
    #             "TextSize": "large",
    #             "TextHAlign": "center",
    #             "TextVAlign": "middle",
    #             "ActionType": "reply",
    #             "ActionBody": "Italian",
    #             "BgColor": "#dd8157",
    #             "Image": "https://s18.postimg.org/x41iip3o5/itallian.png"
    #         }, {
    #             "Columns": 2,
    #             "Rows": 2,
    #             "Text": "<br><font color=\"#494E67\"><b>INDIE</b></font>",
    #             "TextSize": "large",
    #             "TextHAlign": "center",
    #             "TextVAlign": "middle",
    #             "ActionType": "reply",
    #             "ActionBody": "Indie",
    #             "BgColor": "#f6f7f9",
    #             "Image": "https://s18.postimg.org/wq06j3jkl/indi.png"
    #         }, {
    #             "Columns": 2,
    #             "Rows": 2,
    #             "Text": "<br><font color=\"#494E67\"><b>MORE</b></font>",
    #             "TextSize": "large",
    #             "TextHAlign": "center",
    #             "TextVAlign": "middle",
    #             "ActionType": "reply",
    #             "ActionBody": "More",
    #             "BgColor": "#a8aaba",
    #             "Image": "https://s18.postimg.org/ylmyu98et/more_Options.png",
    #
    #         }]
    #     }
    #     text_message = TextMessage(text='Это бот')
    #     message = KeyboardMessage(tracking_data='tracking_data', keyboard=SAMPLE_KEYBOARD)
    #
    #     viber.send_messages(viber_request.sender.id, [
    #         text_message, message
    #     ])
    #
    #     if text_type == 'More':
    #         SAMPLE_RICH_MEDIA = {
    #             "BgColor": "#69C48A",
    #             "Buttons": [
    #                 {
    #                     "Columns": 6,
    #                     "Rows": 1,
    #                     "BgColor": "#454545",
    #                     "BgMediaType": "gif",
    #                     "BgMedia": "http://www.url.by/test.gif",
    #                     "BgLoop": "true",
    #                     "ActionType": "open-url",
    #                     "Silent": "true",
    #                     "ActionBody": "www.tut.by",
    #                     "Image": "www.tut.by/img.jpg",
    #                     "TextVAlign": "middle",
    #                     "TextHAlign": "left",
    #                     "Text": "<b>example</b> button",
    #                     "TextOpacity": 10,
    #                     "TextSize": "regular"
    #                 }
    #             ]
    #         }
    #         SAMPLE_ALT_TEXT = "upgrade now!"
    #         message = RichMediaMessage(rich_media=SAMPLE_RICH_MEDIA, alt_text=SAMPLE_ALT_TEXT, min_api_version=2)
    #         viber.send_messages(viber_request.sender.id, [
    #             message
    #         ])
    #         print(viber_request.sender.api_version)
    #
    #     elif text_type == 'Asian':
    #         viber.send_messages(viber_request.sender.id, [
    #             TextMessage(text='Asian')
    #         ])
    #
    #     elif text_type == 'Mexican':
    #         viber.send_messages(viber_request.sender.id, [
    #             TextMessage(text='Mexican')
    #         ])
    #
    #
    # elif isinstance(viber_request, ViberConversationStartedRequest):
    #     print(viber_request)
    #     viber.send_messages(viber_request.user.id, [
    #         TextMessage(text="Welcome!")
    #     ])

    return HttpResponse(status=200)


class ViberUserView(View):
    def get(self, request):
        return HttpResponse('Hi')
