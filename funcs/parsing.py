import csv
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio

# импорт ключей из файла config.py
from config import api_id, api_hash, phone_number, session_name

# функция парсинга каналов, на вход принимает строку, на выход дает файл.csv с постами
async def parsing(chanels_user_input: str): 
    chanels_list = chanels_user_input.split(',')
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start(phone_number)

    # создает новый файл chanel_posts.csv и прописывает в нем колонки
    # при повторном вызове функции удаляет содержимое файла и прописывает заново колонки
    with open("data/raw/chanel_posts_raw.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['chanel', 'link', 'date', 'text'])

    # цикл перебирающий введеные каналы
    for chanel in chanels_list:

        # функция которое переводит строку-название в корутину, которая имеет свои методы для работы
        chanel_entity = await client.get_entity(chanel)

        offset_id = 0
        limit = 100
        total_messages = 0
        total_count_limit = 3000

        # перебираем сообщения по limit (больше 100 нельзя) штук, начиная с offset_id (последнего в данном случае)
        # через total_messages проверяем сколько сообщений уже обработано, если достигаем total_count_limit, то прекращаем обработку функции while
        while True:
            messages = await client(GetHistoryRequest(
                peer=chanel_entity,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))

            # если в канале не осталось сообщений, то прерываем функцию while
            if not messages.messages:
                break

            # берем 100 постов из канала, если в посте есть текст, то добавляем данные о нем в файл chanel_posts.csv
            for message in messages.messages:
                if message.message:
                    post_link = 'https://t.me/' + chanel[1:] + '/' + str(message.id)
                    post_text = message.message
                    post_date = message.date.replace(tzinfo=None)
                    with open("data/raw/chanel_posts_raw.csv", "a", encoding='UTF-8') as f:
                        writer = csv.writer(f, delimiter=",", lineterminator="\n")
                        writer.writerow([chanel, post_link, post_date, post_text])
            offset_id = messages.messages[-1].id
            total_messages += limit
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        # добавляем паузу между парсингом каналов, чтобы тг не начал рвать сессии
        await asyncio.sleep(5)

    await client.disconnect()


