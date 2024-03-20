import streamlit as st
import pandas as pd
from utils.preprocessing import filter_df
from .individual_stats_tab import selector_component



def select_component(df: pd.DataFrame):
    col1,col2,col3=st.columns(3)
    with col1:
        brand = st.selectbox(
        'Бренд',
        df['Brands'].unique(), key="1")
    with col2:
        status = st.multiselect(
        'Статус', ['запущена','остановлена'],
        [], key="2")     
    with col3:
        id_ = st.text_input('Поиск по ID',max_chars=df['id'].astype('str').str.len().max(), key="3")

    col4,col5,col6=st.columns(3)
    with col4:
        q = st.multiselect(
        'Квартал',
        ['q1', 'q2', 'q3', 'q4'],
        [], key="4")
    with col5:
        sites = df['sites'].unique()
        site = st.multiselect(
        'Площадки',
        sites,
        [], key="5")
    with col6:
        formats = df['Ad copy format'].unique()
        format = st.multiselect(
        'Формат',
        formats,
        [], key="6")
    
    return brand, site, format, status, q, id_


def simple_stats_component(df):
    brand, site, format, status, q, id_ = select_component(df)
    df = filter_df(df,brand,site,format,status,q,id_)
    show_df = df.copy()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Показы", int(df["Viewable impressions (fact)"].mean()))
    col2.metric("Охват", int(df["Reach 1+ (fact)"].mean()))
    col3.metric("Клики", int(df["Click (fact)"].mean()))
    col4.metric("CTR", df["CTR % (fact)"].mean())
    

    show_df = show_df[[
            "id", 
            "Brands", 
            "Viewable impressions (fact)", 
            "Reach 1+ (fact)",
            "Click (fact)",
            "CTR % (fact)"
        ]]

    #Попытался сделать рандомную смену цветов
    """
    for col in background_col:
        df[col] = df[col].to_frame().style.background_gradient(cmap='PuBu')
    """
    background_col = show_df.keys()[2:6]
    show_df = show_df.style.background_gradient(subset=background_col, cmap='YlGn')
    st.write("### Обзор", 
        show_df)
