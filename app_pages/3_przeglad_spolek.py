import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.title("Przegląd wartości wskaźników finansowych spółek")
st.write("Narzędzie do identyfikacji spółek o wysokim potencjale wzrostu.")

latest_data = st.session_state.latest_data
latest_data = latest_data.sort_values(by='Ticker')

# Konfiguracja tabeli AgGrid
gb = GridOptionsBuilder.from_dataframe(latest_data)
gb.configure_default_column(editable=True, groupable=True, filter=True, sortable=True)
# gb.configure_pagination(paginationAutoPageSize=True)  # automatyczne strony
gb.configure_side_bar()  # panel boczny z opcjami filtrowania/sortowania

grid_options = gb.build()

AgGrid(
    latest_data,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.NO_UPDATE,
    enable_enterprise_modules=True,
    theme="streamlit",  
    height=600
    )
