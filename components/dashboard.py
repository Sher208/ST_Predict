import streamlit as st
from components.prediction import prediction
from components.inputs import input_main
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

        prediction(dataframe=dataframe, period=period)
        



    


