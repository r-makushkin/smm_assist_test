import streamlit as st
import plotly.express as px
import pandas as pd


df = pd.read_csv('data/proceed/posts_after_models_1801.csv')

# Преобразование числовых значений в текстовые
df['predicted_class'] = df['predicted_class'].map({0: 'нейтральный', 1: 'позитивный', 2: 'негативный'})

# Подсчет количества значений для каждого класса в 'predicted_class' после преобразования
class_counts = df['predicted_class'].value_counts().reset_index()
class_counts.columns = ['Класс', 'Количество']

# Стандартные и кастомные цветовые схемы
color_schemes = {
    "Plotly": px.colors.qualitative.Plotly,
    "G10": px.colors.qualitative.G10,
    "T10": px.colors.qualitative.T10,
    "D3": px.colors.qualitative.D3,
    "Pastel": px.colors.qualitative.Pastel,
    "Dark24": px.colors.qualitative.Dark24,
    "Пастельная кастомная": {'нейтральный': 'lightgrey', 'позитивный': 'lightgreen', 'негативный': 'lightcoral'}
}

# Выбор цветовой схемы
color_scheme = st.selectbox(
    "Выберите цветовую схему графика:",
    list(color_schemes.keys())
)

# Выбор типа графика
chart_type = st.selectbox(
    "Выберите тип графика:",
    ["Столбчатая диаграмма", "Круговая диаграмма"]
)

# Построение выбранного типа графика
if chart_type == "Столбчатая диаграмма":
    if color_scheme == "Пастельная кастомная":
        fig = px.bar(class_counts, x='Класс', y='Количество', title='Распределение классов по всей базе',
                     color='Класс', color_discrete_map=color_schemes[color_scheme])
    else:
        fig = px.bar(class_counts, x='Класс', y='Количество', title='Распределение классов по всей базе',
                     color='Класс', color_discrete_sequence=color_schemes[color_scheme])
elif chart_type == "Круговая диаграмма":
    if color_scheme == "Пастельная кастомная":
        fig = px.pie(class_counts, names='Класс', values='Количество', title='Распределение классов по всей базе',
                     color='Класс', color_discrete_map=color_schemes[color_scheme])
    else:
        fig = px.pie(class_counts, names='Класс', values='Количество', title='Распределение классов по всей базе',
                     color='Класс', color_discrete_sequence=color_schemes[color_scheme])

# Вывод графика в Streamlit
st.plotly_chart(fig)

user_input = st.text_input("Введите два бренда, разделенных пробелом", "Аэрофлот s7")

# Разделение ввода на два бренда
brands = user_input.split()
if len(brands) >= 2:
    brand1, brand2 = brands[0], brands[1]

    # Фильтрация DataFrame для строк с упоминанием первого бренда
    df_1 = df[df['text'].str.contains(brand1, case=False, na=False)]

    # Фильтрация DataFrame для строк с упоминанием второго бренда
    df_2 = df[df['text'].str.contains(brand2, case=False, na=False)]

# Подсчет количества упоминаний брендов по каналам
channel_counts_1 = df_1['chanel'].value_counts().reset_index()
channel_counts_1.columns = ['Канал', 'Количество']

channel_counts_2 = df_2['chanel'].value_counts().reset_index()
channel_counts_2.columns = ['Канал', 'Количество']

# Создание графиков с использованием Plotly
if color_scheme == "Пастельная кастомная":
    color_discrete_map = color_schemes[color_scheme]
else:
    color_discrete_sequence = color_schemes[color_scheme]

fig1 = px.bar(channel_counts_1, x='Канал', y='Количество', 
              title=f'Распределение упоминаний<br>{brand1} по каналам',
              color_discrete_sequence=color_discrete_sequence if color_scheme != "Пастельная кастомная" else None,
              color='Канал' if color_scheme == "Пастельная кастомная" else None,
              color_discrete_map=color_discrete_map if color_scheme == "Пастельная кастомная" else None)
fig1.update_layout(xaxis_title='Канал', yaxis_title='Количество', xaxis_tickangle=-45)

fig2 = px.bar(channel_counts_2, x='Канал', y='Количество', 
              title=f'Распределение упоминаний<br>{brand2} по каналам',
              color_discrete_sequence=color_discrete_sequence if color_scheme != "Пастельная кастомная" else None,
              color='Канал' if color_scheme == "Пастельная кастомная" else None,
              color_discrete_map=color_discrete_map if color_scheme == "Пастельная кастомная" else None)
fig2.update_layout(xaxis_title='Канал', yaxis_title='Количество', xaxis_tickangle=-45)

# Вывод графиков в Streamlit
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)

# Подсчет количества упоминаний брендов по каналам
channel_counts_1 = df_1['chanel'].value_counts().reset_index()
channel_counts_1.columns = ['Канал', f'Упоминания {brand1}']

channel_counts_2 = df_2['chanel'].value_counts().reset_index()
channel_counts_2.columns = ['Канал', f'Упоминания {brand2}']

# Объединение данных об упоминаниях брендов
combined_channel_counts = channel_counts_1.merge(channel_counts_2, on='Канал', how='outer')

# Создание графика с использованием Plotly
fig = px.bar(combined_channel_counts, x='Канал', 
             y=[f'Упоминания {brand1}', f'Упоминания {brand2}'], 
             title=f'Сравнение упоминаний брендов по каналам',
             color_discrete_sequence=color_schemes[color_scheme] if color_scheme != "Пастельная кастомная" else None,
             color_discrete_map=color_schemes[color_scheme] if color_scheme == "Пастельная кастомная" else None)

fig.update_layout(xaxis_title='Канал', yaxis_title='Количество упоминаний', xaxis_tickangle=-45)

# Вывод графика в Streamlit
st.plotly_chart(fig, use_container_width=True)

st.write(df_2.head(5))

# Подсчет тональности отзывов для каждого бренда
sentiment_counts_1 = df_1['predicted_class'].value_counts().reset_index()
sentiment_counts_1.columns = ['Тональность', f'Количество {brand1}']

sentiment_counts_2 = df_2['predicted_class'].value_counts().reset_index()
sentiment_counts_2.columns = ['Тональность', f'Количество {brand2}']

if color_scheme == "Пастельная кастомная":
    fig1 = px.pie(sentiment_counts_1, values=f'Количество {brand1}', names='Тональность', title=f'Тональность отзывов для {brand1}', color_discrete_map=color_schemes[color_scheme])
else:
    fig1 = px.pie(sentiment_counts_1, values=f'Количество {brand1}', names='Тональность', title=f'Тональность отзывов для {brand1}', color_discrete_sequence=color_schemes[color_scheme])

if color_scheme == "Пастельная кастомная":
    fig2 = px.pie(sentiment_counts_2, values=f'Количество {brand2}', names='Тональность', title=f'Тональность отзывов для {brand2}', color_discrete_map=color_schemes[color_scheme])
else:
    fig2 = px.pie(sentiment_counts_2, values=f'Количество {brand2}', names='Тональность', title=f'Тональность отзывов для {brand2}', color_discrete_sequence=color_schemes[color_scheme])

# Вывод графиков в одной строке
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
