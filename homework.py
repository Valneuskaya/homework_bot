from email import message
import os

import sys

import requests

import time

import logging

from dotenv import load_dotenv

import telegram

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, ReplyKeyboardMarkup

from APIError import APIError



load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def log_raise_error(error_message):
    """Логи и вызов исключения"""
    message = f'Программа {error_message} не работает'
    logger.error(message)
    raise APIError(message)


def send_message(bot, message):
    """Отправляет сообщение в чат TELEGRAM_CHAT_ID"""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
    except telegram.TelegramError:
        error_message = f'Не получилось отправить сообщение "{message}".'
    


def get_api_answer(current_timestamp):
    """Делает запрос к эндпоинту API-сервиса
    и преобразует ответ к типам данных Python"""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    homework_statuses = requests.get(
            url=ENDPOINT,
            headers=HEADERS,
            params=params
        )
    return homework_statuses.json()


def check_response(response):
    """Проверяет ответ API на корректность
    и возвращяет список домашних работ."""
    api_homeworks_key = 'homeworks'
    try:
        homeworks = response[api_homeworks_key]
        time_stamp = response['current_date']
    except KeyError as error:
        error_message = f'Ключа {error} нет в ответе API'
    else:
        if not isinstance(homeworks, list):
            error_msg = (
                f'Под ключом {api_homeworks_key} в ответе API '
                f'содержится некорректный тип: {type(homeworks)}'
            )
            #log_and_raise_error(error_msg)
        if not homeworks:
            logger.debug(
                (
                    'Статус домашней работы не изменился '
                    f'с времени UNIX-time: {time_stamp}'
                )
            )
        return homeworks
    


def parse_status(homework):
    """Извлекает статус домашней работы
    и возвращает один из вердиктов словаря HOMEWORK_STATUSES."""
    try:
        homework_name = homework['homework_name']
        homework_status = homework['status']
    except KeyError as error:
        error_message = f'Ключа {error} нет в ответе API'
        log_raise_error(error_message)
    else:
        if homework_status not in HOMEWORK_STATUSES:
            error_message =  (f'Статус {homework_status} '
                            f'работы {homework_name} не найден')
            log_raise_error(error_message)
        verdict = HOMEWORK_STATUSES[homework_status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    ...


def main():
    """Основная логика работы бота."""
    
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    updater = Updater(token=TELEGRAM_TOKEN)
    updater.start_polling(poll_interval=10.0)
    updater.idle()
    ...

    while True:
        try:
            response = ...

            ...

            current_timestamp = ...
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
            time.sleep(RETRY_TIME)
        else:
            ...
    



if __name__ == '__main__':
    main()
