import streamlit as st
from components.prediction import prediction
from components.inputs import input_main
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

def plot_raw_data(data, source):
    fig = go.Figure()
    if source == "Source Input":
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close'))
    else:
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Adj Close'], name='stock_close'))

    fig.layout.update(title_text="Time Series", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)



def body(title = "Stock Data Predictor"):
    st.title(title)
    source = st.radio("Source Input / Manual Input", ('Manual Input','Source Input'))

    dataframe = input_main(source)

    if dataframe is not None:
        plot_raw_data(dataframe, source)

        n_years = st.slider("Months of pridiction", 1, 36)
        period = n_years * 30

        forecast, m = prediction(dataframe=dataframe, period=period)
        
        st.subheader('Forecast data')
        st.write(forecast.tail())

        st.subheader('Forecast Plot')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)

        st.write('Forecast components')
        fig2 = m.plot_components(forecast)
        st.write(fig2)



    


