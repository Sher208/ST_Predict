from fbprophet import Prophet
import streamlit as st

def prediction(dataframe, period):

    df_train = dataframe[['Date', 'Adj Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Adj Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    return forecast, m