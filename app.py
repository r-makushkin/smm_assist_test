import streamlit as st
from st_pages import Page, show_pages

show_pages([
        Page('app.py', 'Главная'),
        Page('pages/user_input_page.py', 'Ввод пользовательской информации'),
        Page('pages/analitycs_page.py', 'Аналитика'),
        Page('pages/results.py', 'Результаты')
])
