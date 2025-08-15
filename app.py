import streamlit as st
import pandas as pd


# ---- Load data ----
if "all_data" not in st.session_state:
    st.session_state.all_data = pd.read_csv(r'Data\app_all_data.csv')
    st.session_state.app_latest_data = pd.read_csv(r'Data\app_latest_data.csv')
    st.session_state.app_yearly_data = pd.read_csv(r'Data\app_yearly_data.csv')

pages = [
    st.Page("app_pages/1_strona_glowna.py", title="Strona główna"),
    st.Page("app_pages/2_wyszukiwarka_spolek.py", title="Wyszukaj spółkę",),
    st.Page("app_pages/3_przeglad_spolek.py", title="Przegląd spółek"),
]

pg = st.navigation(pages, position="sidebar", expanded=True)
pg.run()
