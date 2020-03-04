from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage, KeyboardMessage
from viberbot.api.viber_requests import viber_request

from .models import ViberUser

bot_configuration = BotConfiguration(
    name='Разрулим',
    avatar='http://viber.com/avatar.jpg',
    auth_token='4afeb69babe7d0b5-77a54a34f7862353-9b2e40aba57d9c82')

viber = Api(bot_configuration)


# def registration(v_id):
#     v_user, create = ViberUser.objects.update_or_create(viber_id=v_id,
#                                                         defaults={'is_active': True
#
#                                                                   })
#     if v_user.phone_number is None:
#         SAMPLE_KEYBOARD = {
#             "Type": "keyboard",
#             "Buttons": [
#                 {
#                     "Columns": 6,
#                     "Rows": 2,
#                     "BgLoop": True,
#                     "ActionType": "share-phone",
#                     "ActionBody": "This will be sent to your bot in a callback",
#                     "ReplyType": "message",
#                     "Text": "<font color = ”# 7F00FF”> Push me! < font>"
#                 }
#             ]
#         }
#         text_message = TextMessage(text='Номер принят')
#         keyboard_message = KeyboardMessage(tracking_data='tracking_data', keyboard=SAMPLE_KEYBOARD, min_api_version=3)
#         viber.send_messages(v_user.viber_id, [text_message, keyboard_message])
