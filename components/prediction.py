from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import streamlit as st

def prediction(dataframe, period):

    df_train = dataframe[['Date', 'Adj Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Adj Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.subheader('Forecast Plot')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write('Forecast components')
    fig2 = m.plot_components(forecast)
    st.write(fig2)