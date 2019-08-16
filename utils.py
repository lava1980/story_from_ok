from telegram import KeyboardButton, ReplyKeyboardMarkup

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)    
    my_keyboard = ReplyKeyboardMarkup([                                     
                                    [contact_button]                                   
                                    
                                    ], resize_keyboard=True)

    return my_keyboard


def get_initial_data(update, user_role):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    user_id = update.message.from_user.id
    role = user_role
    initial_user_data = (chat_id, first_name, last_name, user_id, role)
    return initial_user_data

def admin_aprove():
    pass


