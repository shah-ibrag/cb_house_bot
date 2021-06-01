import telebot
from resources import keyboards
from core import db, registeruser, adminUser, client


bot = telebot.TeleBot('')
#db.init_db()
adminUser.new_user(123)
print(db.print_admin_invite())


@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id, 'Введите ваш инвайт-код')
    bot.register_next_step_handler(msg, check_invite)


def check_invite(message):
    responseRegistration = db.use_invite_code(user_invite_code=message.text, user_tg_id=message.chat.id)
    if responseRegistration == True:
        registeruser.new_user(message.chat.id)
        msg = bot.send_message(message.chat.id, 'Добро пожаловать', reply_markup=keyboards.keyboardMainMenu)
        bot.register_next_step_handler(msg, main_menu)
    else:
        msg = bot.send_message(message.chat.id, 'Неверный инвайт-код\nПопробуйте еще раз')
        bot.register_next_step_handler(msg, check_invite)
    if responseRegistration == 'limit = 0':
        msg = bot.send_message(message.chat.id, 'Лимит использования этого инвайт-кода исчерпан\nПопробуйте другой')
        bot.register_next_step_handler(msg, check_invite)



def main_menu(message):
    if message.text == 'Мой инвайт-код':
        msg = bot.send_message(message.chat.id, f'Ваш инвайт код: '
                                                f'<code>{db.select_invite_code(user_tg_id=message.chat.id)}</code>',
                                                parse_mode='html')
        bot.register_next_step_handler(msg, main_menu)
    if message.text == 'Приглашенные':
        print(db.select_invited_users(user_tg_id=message.chat.id))
        for i in db.select_invited_users(user_tg_id=message.chat.id):
            number = 1
            bot.send_message(message.chat.id, f'''<a href='tg://user?id={i}'>Пользователь {number}</a>''', parse_mode='html')
    if message.text == 'Создать комнату':
        msg = bot.send_message(message.chat.id, 'Введите название комнаты: ')
        bot.register_next_step_handler(msg, create_room)

def create_room(message):
    client.create_group(message=message, group_name=message.text, admin_id=message.chat.id)


bot.polling()
