import streamlit as st
import pandas as pd
from nsetools import Nse

from components.utils import generate_payload_for_source, convert_df

from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go



def manual_input():
    st.info("You can insert values of smallcap here")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.text('Here you can upload manual data with Date and Close as the columns (Please include date at index 0 and the closing price at index 1)')
        dataframe = pd.read_csv(uploaded_file)
        adjusted_dataframe = dataframe.rename(columns={dataframe.columns[0]: 'Date',dataframe.columns[1]: 'Adj Close'})
        new_dataframe = adjusted_dataframe[['Date', 'Adj Close']]
        return new_dataframe
    
    return None


def option_input():
    nse = Nse()
    get_symbol = st.text_input("Type the stock to get its pridiction", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="RELIANCE")
    source = st.radio(
        "Select source for the prediction",
        ( 'Yahoo Finance', 'NSE Official Website'))

    if(nse.is_valid_code(get_symbol)):
        data_load_state = st.text("Fetching data....")
        dataframe = generate_payload_for_source(get_symbol, source)
        data_load_state.text("")

        if source == 'NSE Official Website':
            st.info("NSE doesn't seem to contain ajusted closing creating adjusting closing with close")
            dataframe['Close'] = dataframe['CH_CLOSING_PRICE']
            dataframe.rename(columns = {'mTIMESTAMP':'Date', 'CH_CLOSING_PRICE':'Adj Close', 'CH_OPENING_PRICE': 'Open'}, inplace = True)

        return dataframe
    else:
        if get_symbol:
            data_load_state = st.text(get_symbol+ " this index doesn't exists")

    return None


def input_main(source="Source Input"):

    if source == "Source Input" :
        dataframe = option_input()
    elif source == "Manual Input":
        dataframe = manual_input()

    if dataframe is not None:
        st.subheader("Raw header")
        st.write(dataframe.tail(n=5))

        data_for_download = convert_df(dataframe)

        # if get_symbol:
        #     filename = get_symbol+'_DATA.csv'
        # else:
        filename = 'MANUAL.csv'

        st.download_button(
            label="Download data",
            data=data_for_download,
            file_name=filename,
            mime='text/csv',
        )

        return dataframe
    
    return pd.DataFrame()