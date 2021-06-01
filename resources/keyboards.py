import telebot

keyboardMainMenu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttonsMainMenu = [['Создать комнату'], ['Мой инвайт-код'], ['Приглашенные']]
for item in buttonsMainMenu:
    keyboardMainMenu.add(*item)
