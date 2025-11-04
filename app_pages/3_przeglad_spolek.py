import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode

st.title("Przegląd wartości wskaźników finansowych spółek")
st.write("Narzędzie do identyfikacji spółek o wysokim potencjale wzrostu.")

latest_data = st.session_state.latest_data
latest_data = latest_data.sort_values(by='Ticker')

gb = GridOptionsBuilder.from_dataframe(latest_data)
gb.configure_default_column(
    editable=True,
    groupable=True,
    filter=True,
    sortable=True,
    minWidth=120,
    wrapHeaderText=True,
    autoHeaderHeight=True
)
gb.configure_side_bar()

grid_options = gb.build()

AgGrid(
    latest_data,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.NO_UPDATE,
    enable_enterprise_modules=True,
    theme="streamlit",
    height=600,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
    fit_columns_on_grid_load=True
)
