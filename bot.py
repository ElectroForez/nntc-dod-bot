import telebot
from config import BOT_TOKEN
from nn import analyse_string

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message, res=False):
    fullname = get_fullname(message)
    text = f'Привет, {fullname}! Очень рады тебя видеть на дне открытых дверей! ' \
           f'\nНапиши текст для анализа'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["help"])
def send_help(message, res=False):
    help_text = f"""
Напиши текст для анализа.
    
По вопросам ждём здесь:
https://nntc.nnov.ru/

Если вдруг захотелось узнать как сделан бот, то тебе сюда:

""".strip()  # стираем пустые символы по краям
    bot.send_message(message.chat.id, help_text)


def get_fullname(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    fullname = f"{first_name} {last_name}" if last_name else first_name
    return fullname


@bot.message_handler(content_types=["text"])
def send_help(message, res=False):
    analyse_result = analyse_string(message.text)
    translated_result = translate_analyse_result(analyse_result)
    bot.send_message(message.chat.id, translated_result)


def translate_analyse_result(result):
    total_msg = 'Результат анализа:\n'
    total_msg += f'Позитивно на {to_fixed(result["positive"], 2)} %\n' if "positive" in result else ''
    total_msg += f'Негативно на {to_fixed(result["negative"], 2)} %\n' if "negative" in result else ''
    total_msg += f'Нейтрально на {to_fixed(result["neutral"], 2)} %\n' if "neutral" in result else ''
    total_msg += f'Содержание не влияющее на окраску - {to_fixed(result["skip"], 2)} %\n' if "skip" in result else ''
    return total_msg


def to_fixed(numObj, digits=0):
    return f"{numObj * 100:.{digits}f}"


# запускаем бота
bot.polling(none_stop=True, interval=0)