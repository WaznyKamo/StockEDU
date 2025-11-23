import streamlit as st

st.set_page_config(page_title="Strona główna", layout="wide")

st.title("🏠 Strona główna")

st.header("Najbardziej niedowartościowane spółki:", divider="blue")
st.subheader("Spółki z najniższym wskaźnikiem Cena/Zysk")

latest_data = st.session_state.latest_data
st.dataframe(latest_data.sort_values(by='Cena/Zysk [-]', ascending=True).head(8))

st.subheader("Spółki z najniższym wskaźnikiem Cena/Wartość Księgowa")
st.dataframe(latest_data.sort_values(by='Cena/WK [-]', ascending=True).head(8))

st.header("Spółki z technicznym sygnałem silnego zakupu:", divider="blue")
technical_data = st.session_state.technical_data
silne_kupuj = technical_data[technical_data['Overall_signal'] == 'Silne kupuj'][['Ticker', 'RSI_signal', 'MACD_signal', 'BB_signal', 'CCI_signal', 'Stochastic_signal', 'Overall_signal']]
silne_kupuj.rename(columns={
    'Ticker': 'Ticker',
    'RSI_signal': 'Sygnał RSI',
    'MACD_signal': 'Sygnał MACD',
    'BB_signal': 'Sygnał Wstęgi Bollingera',
    'CCI_signal': 'Sygnał CCI (Commodity Channel Index)',
    'Stochastic_signal': 'Sygnał Oscylatora Stochastycznego',
    'Overall_signal': 'Ogólny sygnał'
}, inplace=True)
st.dataframe(silne_kupuj)
