import telebot
from telebot import types

API_TOKEN = '7846162374:AAFgq54q5gYcRt3Gw7MmKGzR6wcFcDrNBN8'
bot = telebot.TeleBot(API_TOKEN)

user_language = {}  # Dictionary to store user language preference
pending_feedback = {}  # Dictionary to track if a user is in feedback mode

def set_language(message):
    markup = types.InlineKeyboardMarkup()
    
    markup.add(types.InlineKeyboardButton('Українська', callback_data='ukrainian'),
               types.InlineKeyboardButton('English', callback_data='english'),
               types.InlineKeyboardButton('Deutsch', callback_data='german'))
    
    bot.send_message(message.chat.id, "Виберіть мову / Choose your language / Wählen Sie Ihre Sprache:", reply_markup=markup)

# 2. Handling language selection and setting language preference
@bot.callback_query_handler(func=lambda call: call.data in ['ukrainian', 'english', 'german'])
def handle_language_selection(call):
    if call.data == 'ukrainian':
        user_language[call.message.chat.id] = 'Українська'
    elif call.data == 'english':
        user_language[call.message.chat.id] = 'English'
    elif call.data == 'german':
        user_language[call.message.chat.id] = 'Deutsch'
    
    send_main_menu(call.message, greet=True)

# 3. Main menu (supports 3 languages)
def send_main_menu(message, greet=False, show_options=True):
    lang = user_language.get(message.chat.id, 'English')
    
    if greet:
        if lang == "Українська":
            greet_msg = "Ласкаво просимо до Roshen Bot!"
        elif lang == "Deutsch":
            greet_msg = "Willkommen beim Roshen Bot!"
        else:
            greet_msg = "Welcome to Roshen Bot!"
        bot.send_message(message.chat.id, greet_msg)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    
    if lang == 'Українська':
        product_button = 'Продукція'
        feedback_button = 'Відправити відгук'
        about_button = 'Про Roshen'
        change_language_button = 'Змінити мову'
    elif lang == 'Deutsch':
        product_button = 'Produkte'
        feedback_button = 'Feedback senden'
        about_button = 'Über Roshen'
        change_language_button = 'Sprache ändern'
    else:
        product_button = 'Products'
        feedback_button = 'Send Feedback'
        about_button = 'About Roshen'
        change_language_button = 'Change Language'
    
    markup.add(product_button, feedback_button, about_button, change_language_button)
    
    if show_options:
        if lang == 'Українська':
            bot.send_message(message.chat.id, "Оберіть опцію:", reply_markup=markup)
        elif lang == 'Deutsch':
            bot.send_message(message.chat.id, "Wählen Sie eine Option:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Select an option:", reply_markup=markup)

# 4. Greeting and language choice
@bot.message_handler(commands=['start'])
def start(message):
    set_language(message)

@bot.message_handler(commands=['inform'])
def inform_user(message):
    markup = types.InlineKeyboardMarkup()
    inform_button = types.InlineKeyboardButton("Дізнатися більше", callback_data='inform_details')
    markup.add(inform_button)
    bot.send_message(message.chat.id, "Натисніть кнопку нижче, щоб отримати інформацію.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'inform_details')
def inform_details(call):
    bot.send_photo(call.message.chat.id, 'https://www.roshen.com/uploads/content/2018/04/17/source/2-min-45x.jpg')

# 5. Command to change language
@bot.message_handler(func=lambda message: message.text in ["Змінити мову", "Change Language", "Sprache ändern"])
def change_language(message):
    set_language(message)

# 6. About Roshen command (supports 3 languages)
@bot.message_handler(func=lambda message: message.text in ["Про Roshen", "About Roshen", "Über Roshen"])
def about_roshen(message):
    lang = user_language.get(message.chat.id, 'English')  # Default to English if no language is set

    if lang == "Українська":
        info_msg = (
            "Корпорація ROSHEN входить до числа найбільших світових виробників кондитерських виробів. "
            "Виробнича потужність усіх фабрик корпорації становить 300 тис. тонн продукції на рік. "
            "Детальніше тут: https://www.roshen.com/ua/en/"
        )
    elif lang == "Deutsch":
        info_msg = (
            "Die ROSHEN Corporation gehört zu den größten Süßwarenherstellern der Welt. "
            "Die Produktionskapazität aller Fabriken beträgt 300.000 Tonnen pro Jahr. "
            "Mehr erfahren Sie hier: https://www.roshen.com/ua/en/"
        )
    else:
        info_msg = (
            "ROSHEN Corporation is one of the largest confectionery manufacturers in the world. "
            "The total production capacity of all factories reaches 300 thousand tons of products per year. "
            "Learn more here: https://www.roshen.com/ua/en/"
        )
    
    bot.send_message(message.chat.id, info_msg)

# 7. Show products submenu (supports 3 languages)
@bot.message_handler(func=lambda message: message.text in ["Продукція", "Products", "Produkte"])
def show_products(message):
    lang = user_language.get(message.chat.id, 'English')
    markup = types.InlineKeyboardMarkup()

    if lang == 'Українська':
        buttons = [
            types.InlineKeyboardButton('Вафлі та Печиво', callback_data='biscuits'),
            types.InlineKeyboardButton('Бісквіти та Рулети', callback_data='sponge_cakes'),
            types.InlineKeyboardButton('Торти', callback_data='cakes'),
            types.InlineKeyboardButton('Цукерки', callback_data='candies'),
            types.InlineKeyboardButton('Шоколад', callback_data='chocolates'),

        ]
    elif lang == 'Deutsch':
        buttons = [
            types.InlineKeyboardButton('Waffeln & Kekse', callback_data='biscuits'),
            types.InlineKeyboardButton('Biskuitkuchen & Rollen', callback_data='sponge_cakes'),
            types.InlineKeyboardButton('Kuchen', callback_data='cakes'),
            types.InlineKeyboardButton('Süßigkeiten', callback_data='candies'),
            types.InlineKeyboardButton('Schokolade', callback_data='chocolates')
         
        ]
    else:
        buttons = [
            types.InlineKeyboardButton('Biscuits & Wafers', callback_data='biscuits'),
            types.InlineKeyboardButton('Sponge Cakes & Rolls', callback_data='sponge_cakes'),
            types.InlineKeyboardButton('Cakes', callback_data='cakes'),
            types.InlineKeyboardButton('Candies', callback_data='candies'),
            types.InlineKeyboardButton('Chocolate', callback_data='chocolates')
        ]

    markup.row(*buttons[:2])
    markup.row(*buttons[2:5])

    product_msg = {
        'Українська': "Оберіть категорію продуктів:",
        'Deutsch': "Wählen Sie eine Produktkategorie:",
        'English': "Select a product category:"
    }.get(lang, "Select a product category:")

    bot.send_message(message.chat.id, product_msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data in ['cakes', 'candies', 'chocolates', 'biscuits', 'sponge_cakes']:
        product_details(call)

def product_details(call):
    lang = user_language.get(call.message.chat.id, 'English')
    
    if call.data == 'cakes':
        if lang == "Українська":
            details_msg = "Торти Roshen: виготовлені з найкращих інгредієнтів. Детальніше тут: https://www.roshen.com/en/cakes"
        elif lang == "Deutsch":
            details_msg = "Roshen Kuchen: Hergestellt aus den besten Zutaten. Mehr erfahren Sie hier: https://www.roshen.com/en/cakes"
        else:
            details_msg = "Roshen Cakes: Made from the finest ingredients. Learn more here: https://www.roshen.com/en/cakes"
    
    elif call.data == 'candies':
        if lang == "Українська":
            details_msg = "Цукерки Roshen: солодкий вибір. Детальніше тут: https://www.roshen.com/en/caramel-and-candies"
        elif lang == "Deutsch":
            details_msg = "Roshen Süßigkeiten: Eine süße Auswahl. Mehr erfahren Sie hier: https://www.roshen.com/en/caramel-and-candies"
        else:
            details_msg = "Roshen Candies: A sweet selection. Learn more here: https://www.roshen.com/en/caramel-and-candies"

    elif call.data == 'chocolates':
        if lang == "Українська":
            details_msg = "Шоколад Roshen: насичений смак та найкращі інгредієнти. Детальніше тут: https://www.roshen.com/en/chocolates-and-chocolate-bars"
        elif lang == "Deutsch":
            details_msg = "Roshen Schokolade: Reich an Geschmack und aus den besten Zutaten hergestellt. Mehr erfahren Sie hier: https://www.roshen.com/en/chocolates-and-chocolate-bars"
        else:
            details_msg = "Roshen Chocolate: Rich in flavor and made from the finest ingredients. Learn more here: https://www.roshen.com/en/chocolates-and-chocolate-bars"
    
    elif call.data == 'biscuits':
        if lang == "Українська":
            details_msg = "Вафлі та Печиво Roshen: широкий вибір хрустких вафель та печива. Детальніше тут: https://www.roshen.com/en/biscuits-and-wafers"
        elif lang == "Deutsch":
            details_msg = "Roshen Waffeln & Kekse: Eine große Auswahl an knusprigen Waffeln und Keksen. Mehr erfahren Sie hier: https://www.roshen.com/en/biscuits-and-wafers"
        else:
            details_msg = "Roshen Biscuits & Wafers: A wide variety of crispy wafers and biscuits. Learn more here: https://www.roshen.com/en/biscuits-and-wafers"

    elif call.data == 'sponge_cakes':
        if lang == "Українська":
            details_msg = "Бісквіти та Рулети Roshen: м'які бісквіти і смачні рулети. Детальніше тут: https://www.roshen.com/en/sponge-cakes-and-rolls"
        elif lang == "Deutsch":
            details_msg = "Roshen Biskuitkuchen & Rollen: Weiche Biskuitkuchen und leckere Rollen. Mehr erfahren Sie hier: https://www.roshen.com/en/sponge-cakes-and-rolls"
        else:
            details_msg = "Roshen Sponge Cakes & Rolls: Soft sponge cakes and delicious rolls. Learn more here: https://www.roshen.com/en/sponge-cakes-and-rolls"
    
    else:
        if lang == "Українська":
            details_msg = "Вибачте, інформація про продукт недоступна."
        elif lang == "Deutsch":
            details_msg = "Entschuldigung, Produktinformationen sind nicht verfügbar."
        else:
            details_msg = "Sorry, product information is not available."
    
    try:
        bot.answer_callback_query(call.id)  
    except Exception as e:
        print(f"Error answering callback query: {e}")

    bot.send_message(call.message.chat.id, details_msg)

# 9. Feedback handling with cancel option
@bot.message_handler(func=lambda message: message.text in ["Відправити відгук", "Send Feedback", "Feedback senden"])
def request_feedback(message):
    lang = user_language.get(message.chat.id, 'English')
    feedback_msg = (
        "Будь ласка, завантажте фото, відео, аудіо або текст вашого відгуку:" if lang == 'Українська' else
        "Bitte laden Sie Ihr Foto, Video, Audio oder Text hoch:" if lang == "Deutsch" else
        "Please upload your photo, video, audio, or text feedback:"
    )
    
    pending_feedback[message.chat.id] = True 
    
    bot.send_message(message.chat.id, feedback_msg)

@bot.message_handler(content_types=['photo', 'video', 'audio', 'document', 'text'])
def handle_feedback(message):
    if pending_feedback.get(message.chat.id, False): 
        lang = user_language.get(message.chat.id, 'English')
        
        
        thanks_msg = 'Дякуємо за ваш відгук!' if lang == 'Українська' else 'Danke für Ihr Feedback!' if lang == 'Deutsch' else 'Thank you for your feedback!'
        bot.reply_to(message, thanks_msg)
        
        pending_feedback[message.chat.id] = False
        send_main_menu(message, greet=False, show_options=False)

bot.polling(none_stop=True)
