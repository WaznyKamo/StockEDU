import streamlit as st

st.set_page_config(page_title="Strona główna", layout="wide")

st.title("Strona główna")

st.header("Najbardziej niedowartościowane spółki:", divider="blue")
st.subheader("Spółki z najniższym wskaźnikiem Cena/Zysk")

app_latest_data = st.session_state.app_latest_data
st.dataframe(app_latest_data.sort_values(by='Cena/Zysk [-]', ascending=True).head())

st.subheader("Spółki z najniższym wskaźnikiem Cena/Wartość Księgowa")
st.dataframe(app_latest_data.sort_values(by='Cena/WK [-]', ascending=True).head())