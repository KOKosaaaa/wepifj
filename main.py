import telebot
from telebot import types
import requests
from io import BytesIO


bot = telebot.TeleBot('6706463621:AAFed1hCxdL-_rU1kQ7LxYrDNloluATQJJY')


game_structure = {
    'levels': {
        'level1': {
            'locations': {
                'location1': {
                    'description': 'Вы находитесь в деревне.',
                    'illustration': 'https://gas-kvas.com/grafic/uploads/posts/2023-09/1695858601_gas-kvas-com-p-kartinki-derevnya-4.jpg',
                    'actions': {
                        'Идти в лес': 'https://sportishka.com/uploads/posts/2022-03/1646300938_44-sportishka-com-p-lesa-v-daleke-turizm-krasivo-foto-67.jpg',
                        'Посетить таверну': 'https://i.ytimg.com/vi/-DOPaKAFkD8/maxresdefault.jpg',
                    }
                },
                'level1_location2': {
                    'description': 'Вы в лесу.',
                    'illustration': 'https://catherineasquithgallery.com/uploads/posts/2021-03/1614624765_2-p-fon-lesa-dlya-fotoshopa-2.jpg',
                    'actions': {

                        'Вернуться в деревню': 'location1',
                    }
                },
                'level1_location3': {
                    'description': 'Вы в таверне.',
                    'illustration': 'https://i.ytimg.com/vi/-DOPaKAFkD8/maxresdefault.jpg',
                    'actions': {
                        'Поговорить с тавернщиком': 'https://chakiris.club/uploads/posts/2022-11/1668932810_chakiris-club-p-traktirshchik-art-pinterest-1.jpg',
                        'Вернуться в деревню': 'location1',
                    }
                },
                'level1_location4': {
                    'description': 'Вы находите приключения.',
                    'illustration': 'https://mir-s3-cdn-cf.behance.net/project_modules/1400/7381f677205107.5c80b969a9889.jpg',
                    'actions': {
                        'Вернуться в деревню': 'location1',
                    }
                },
                'level1_location5': {
                    'description': 'Тавернщик рассказывает вам истории.',
                    'illustration': 'https://chakiris.club/uploads/posts/2022-11/1668932810_chakiris-club-p-traktirshchik-art-pinterest-1.jpg',
                    'actions': {
                        'Вернуться в деревню': 'location1',
                    }
                },
            }
        }
    }
}


user_states = {}

# Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    user_states[user_id] = {'level': 'level1', 'location': 'location1'}
    send_location_description(user_id)

# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    user_id = message.chat.id
    user_state = user_states.get(user_id)

    if user_state:
        level = user_state['level']
        location = user_state['location']

        print("DEBUG: Received message:", message.text)
        print("DEBUG: Current user state:", user_state)

        if message.text in game_structure['levels'][level]['locations'][location]['actions']:
            if message.text == 'Идти в лес':
                bot.send_message(user_id, 'Вы направляетесь в лес.')
                user_states[user_id]['location'] = 'level1_location2'
                send_location_description(user_id)
            elif message.text == 'Посетить таверну':
                bot.send_message(user_id, 'Вы идете в таверну.')
                user_states[user_id]['location'] = 'level1_location3'
                send_location_description(user_id)
            elif message.text == 'Поговорить с тавернщиком':
                bot.send_message(user_id, 'Тавернщик рассказывает вам истории.')
                user_states[user_id]['location'] = 'level1_location5'
                bot.send_message(user_id, 'Теперь вы можете вернуться в деревню.')
            elif message.text == 'Вернуться в деревню':
                bot.send_message(user_id, 'Вы возвращаетесь в деревню.')
                user_states[user_id]['location'] = 'location1'
                send_location_description(user_id)


def send_location_description(user_id):
    user_state = user_states.get(user_id)
    if user_state:
        level = user_state['level']
        location = user_state['location']
        description = game_structure['levels'][level]['locations'][location]['description']
        illustration_url = game_structure['levels'][level]['locations'][location]['illustration']

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        actions = game_structure['levels'][level]['locations'][location]['actions'].keys()
        markup.add(*actions)

        bot.send_photo(user_id, illustration_url, caption=description, reply_markup=markup, timeout=30)


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
