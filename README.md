# Python telegram bot

Написан Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнает статус домашней работы: 
  
- взята ли она в ревью,
- проверена ли она,
- а если проверена — то принял её ревьюер или вернул на доработку.

Что бот умеет:

- раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram;
- логирует свою работу (дата и время события, уровень важности события, описание события) и сообщает о важных проблемах сообщением в Telegram.
