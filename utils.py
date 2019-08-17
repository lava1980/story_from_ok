import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegraph import Telegraph

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)    
    my_keyboard = ReplyKeyboardMarkup([                                     
                                    [contact_button]                                   
                                    
                                    ], resize_keyboard=True)

    return my_keyboard


def get_inline_keyboard():
    inlinekeyboard = [[InlineKeyboardButton('Да', callback_data='1'),
                        InlineKeyboardButton('Нет', callback_data='2')]]
    kbd_markup = InlineKeyboardMarkup(inlinekeyboard)
    return kbd_markup



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

def handle_text(text):
    text1 = text.replace('\n\n', '<rrrr>')
    text2 = text1.replace('\n', '\n\n')
    text3 = text2.replace('<rrrr>', '\n\n')
    text4 = text3.replace('\n \n', '\n\n')    
    return text4


def text_to_html(text):
    html_text = text.replace('\n', '<br />')
    print(html_text)
    return html_text



def create_telegraph_page(headline, html_content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='14021980')
    response = telegraph.create_page(
        headline, html_content=html_content
    )
    print('https://telegra.ph/{}'.format(response['path']))
    return 'https://telegra.ph/{}'.format(response['path'])


def get_image(filename, foldername):
    path = os.getcwd() + '/images/' + foldername + '/' + filename
    try:
        image = open(path, 'rb')
    except FileNotFoundError:
        image = open(os.getcwd() + '/images/' + foldername + '/noimage.gif', 'rb')
        return image
    return image






if __name__ == "__main__":
    #main()
    handle_text(
        '''Жена моего друга Саши улетела за границу навестить мать, и он пригласил меня на холостяцкий ужин. Когда я приехал, Саша колдовал над сковородкой картошки. \n- Она почему-то прилипает, — озабоченно сказал он. — Странно, раньше этого не было. \nЯ убедился, что дно сковородки уже полностью скрылось под жёлтым слоем. \n- Хорошая, наверно, сковородка. Была, — подчеркнул я глагол. \n- Мне надо ехать за дочерью на автобусную остановку, — сообщил Саша, — а ты пока продолжай перемешивать картошку. \nОн отошёл от плиты и уставился на духовку. \n- Горячие бутерброды, — внезапно закричал он. — Я забыл их нагреть. \nСаша поколдовал над кнопками духовки, оттуда приветливо зажёгся свет, и Саша унёсся. \nЯ задумчиво тормошил картошку, которая прилипала уже не ко дну сковородки, а к прилипшему ранее. Через несколько минут мне это надоело, и я открыл духовку. Меня встретил могильный холод. Я нашёл программу, при которой тепло, судя по значку, идёт только сверху, и прибавил чуток градусов. Духовка откликнулась мгновенным потеплением. \n- Профессионала не обманешь, — объяснил я ей и вернулся к картошке. Теперь она облепила и стенки сковородки. Тут вернулся Саша, и я сдал ему смену. \n- Жареной эта картошка уже не будет, пусть тогда варится, — решил он, накрыл сковородку крышкой и перевёл на маленький огонь. — Пойдём жарить стейки. \nМы вышли во двор, включили мангал и сварганили три стейка медиум. В гостиной нас встретил странный запах. \n- Бутерброды горят! — диагностировали мы спустя какое-то время. \nСаша рванулся к духовке, выхватил из неё горячий противень, и, заорав от боли, швырнул его на столешницу. \n- Что это было, когда это ещё было бутербродом? — осторожно спросил я, глядя на содержание противня. \n- Шпрот, солёный огурец, чеснок и пармезан на чёрном хлебе, — ответил кулинар. \n- То есть, хлеб изначально был чёрным? — обрадовался я и храбро откусил от менее горелой стороны. \n- Ну, как? — опасливо поинтересовался Саша. \n- Ты знаешь, хорошо, — успокоил я друга. — Я, правда, не различаю на вкус, что из них шпрот, а что огурец, но так даже интереснее. \n- Давай садиться, — сказал Саша. — Кстати, салаты уже на столе. Часть я купил, но лучшие сделал сам. Особенно хорош этот, — он указал на миску, где помидоры и лук обильно перемежались чем-то нелогичным. Я вопросительно взглянул на хозяина дома. \n- Инжир, базилик и оливковое масло. Этот салат моя гордость: я сам его изобрёл, — скромно сказал Саша. \n- Хорошо, что ты не только шеф, но и кардиолог, — подбодрил я его. — А где многострадальная картошка? \n- А я её прямо в сковородке сейчас поставлю. \n


        '''
        
        )