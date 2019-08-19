import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegraph import Telegraph
from telegraph.exceptions import TelegraphException

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)    
    my_keyboard = ReplyKeyboardMarkup([                                     
                                    [contact_button]                                   
                                    
                                    ], resize_keyboard=True)

    return my_keyboard


def get_inline_keyboard(bot, inline_data):
    inlinekeyboard = [[InlineKeyboardButton('Да', callback_data='1'),
                        InlineKeyboardButton('Нет', callback_data=inline_data)]]
    kbd_markup = InlineKeyboardMarkup(inlinekeyboard)
    return kbd_markup


def parse_inline_data(data):
    images_list = data.split(', ')
    post_id = images_list.pop(-1)
    if len(images_list) == 0:
        images_list = ''
    return post_id, images_list
    



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
    text2 = text1.replace('\n \n', '<rrrr>')   
    text3 = text2.replace(' \n \n', '<rrrr>')
    text4 = text3.replace('\n', '\n\n')
    text5 = text4.replace('<rrrr>', '\n\n')    
    return text5


def text_to_html(text):
    html_text = text.replace('\n', '<br />')    
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


def delete_images(images_list, foldername):
    for image in images_list:
        path = path = os.getcwd() + '/images/' + foldername + '/' + image
        if os.path.exists(path):
            try:
                os.remove(path)
            except IsADirectoryError:
                print('История в базе без изображения. Удалять нечего.')
        else: print('Нет такого изображения: ' + image)
    


if __name__ == "__main__":
    #main()
    # handle_text(
    #    '''Бойлер\n\nЖил в Японии. У них нет центрального отопления, как у нас. В довольно приличном доме в центре Токио у меня стоит бойлер с мини-компьютером, который делает все сам: включается, отключается, снимает все температурные данные с датчиков, раскиданных по квартире, радует меня десятком подмигивающих лампочек – разве что не разговаривает. Вдруг, посреди февраля (а в Токио это промозглая и до костей пробирающая нулевая сырость) лампочки как-то померкли и заскучали. В доме резко похолодало. Семья моя тоже заскучала: Таймыр по-японски, плюс сквозняки и дети, мотающие сопли на кулак. На бойлере, как положено, пришлепан лейбл компании, обслуживающей это чудо техники. \n \nПозвонил и вызвал мастера. Через пару часов является: в хрустящем от чистоты белоснежном комбинезоне, в белых перчатках, на голове - белая кепка с фирменной кокардой, с огроменной белой сумкой на плече. Я ему объясняю ситуацию – слава Богу, родная страна дала мне приличное образование, и, в отличие от новых русских, догадываюсь, что в японском языке нет такого слова СУШИ, а есть СУСИ, а СУШИ – это калька с английского, - короче, мы поняли друг друга с полуслова. Он понимающе посмотрел на меня, я одобряюще кивнул. Нормально Григорий – отлично Константин. \n \nРабота закипела: из белоснежной сумки был извлечен … нет, не набор инструментов, а фолиант объемом не менее 500 страниц. Этакий "Апостол" Ивана Федорова, представьте себе, в белом переплете. Мой Мастер (далее, исключительно из уважения, с большой буквы) ищет по оглавлению словосочетание "не работает". Находит, ведет пальцем по оглавлению дальше и находит слово "бойлер", ведет пальцем еще дальше и находит маркировку моего бойлера. Минут пять сверяет маркировку с лейблом, затем глубоко вздыхает, лезет в сумку и достает…второй том "Апостола". Снова поиски по оглавлению, шелест страниц, как шелест знамен, снова знакомый тяжелый вздох, и из сумки извлекается…третий том "Апостола". Затем все три тома аккуратно раскладываются на полу и начинается самое интересное. Поскольку японский язык, как уже упоминалось, мне немного знаком, я с интересом наблюдаю за картинкой: 375-я страница первого тома отсылает его к 132-й странице 3-го тома, которая, в свою очередь, шлет его к 367-й странице 2-го тома, а та – опять к первому тому, но уже к 56-й странице. И так далее… Прикинув, что полторы тысячи страниц – это почти "Война и мир" Толстого, я вежливо предложил Мастеру перебазироваться из узкого и темного коридора на кухню, заварил кофе, сдвинул кухонный стол, и мы с ним в течение 2,5 часов на кухонном полу вместе с огромным интересом изучали мой бойлер по картинкам, схемам и техническим руководствам. В мои обязанности входило нахождение соответствующих ссылок в очередном томе "Апостола". Периодически он вскакивал, подбегал к бойлеру, и из коридора до меня доносилось оморфопоэтическое наречие: "Са-а-а-а", что в переводе с японского (в зависимости от контекста) означает очень многое (Ну, вы понимаете). \n \nКороче, по прошествии трех часов он аккуратно собрал все три тома, дико извиняясь, вежливо раскланялся и посоветовал мне обратиться к компании-производителю бойлеров, объяснив, что такой ремонт для них слишком сложен. \n \nВозвращается жена с ребенком. В доме разве что инея на стенах нет. Я рассказываю ей историю про Мастера. Она с ностальгией вспоминает сантехника Колю в Москве и бросает фразу: "Мужик ты, или не мужик. Сделай же что-нибудь". \n \nИду к бойлеру, бью по нему кулаком


    #    '''
        
    #    )
    data = '777778887699-1.webp, 777778887699-2.webp, 777778887699'
    parse_inline_data(data)
        