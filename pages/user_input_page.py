import streamlit as st
from funcs.parsing import parsing
from funcs.data_processing import get_data
import asyncio


st.title("Streamlit App")

# Ввод переменных от пользователя
chanel_user_input = st.text_input("Введите каналы для отслеживания", "")
keyword_user_input = st.text_input("Введите ключ для отслеживания", "")


# Кнопка для запуска внешнего скрипта
if st.button("Сделать выгрузку постов"):
    asyncio.run(parsing(chanel_user_input))

if st.button('Обработка данных нейросетью'):
    get_data('data/raw/chanel_posts_raw_cut.csv')