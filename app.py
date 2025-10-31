import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aplikacja Finansowa", layout="wide")
st.logo("Utils/stockedu.svg", size="large")

# ---- Load data ----
if "all_data" not in st.session_state:
    st.session_state.all_data = pd.read_csv(r'Data/app_all_data.csv')
    st.session_state.latest_data = pd.read_csv(r'Data/app_latest_data.csv')
    st.session_state.yearly_data = pd.read_csv(r'Data/app_yearly_data.csv')
    st.session_state.daily_data = pd.read_csv(r'Data/app_all_daily_data.csv')
    st.session_state.technical_data = pd.read_csv(r'Data/app_technical_indicators.csv')
    

pages = [
    st.Page("app_pages/1_strona_glowna.py", title="Strona główna", icon="🏠"),
    st.Page("app_pages/2_wyszukiwarka_spolek.py", title="Wyszukaj spółkę", icon="🔍"),
    st.Page("app_pages/3_przeglad_spolek.py", title="Przegląd spółek", icon="📋")
]

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()
