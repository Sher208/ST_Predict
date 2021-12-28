from nsepython import *
import streamlit as st
import yfinance as yf
from datetime import date, datetime, timedelta

logging.basicConfig(level=logging.DEBUG)

START = datetime.strptime("01-01-2015","%d-%m-%Y").date()
TODAY = datetime.strptime(date.today().strftime("%d-%m-%Y"), "%d-%m-%Y").date()

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

@st.cache
def equity_history_virgin_nse(symbol,start_date,end_date, series='EQ'):
    url="https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+str(start_date)+"&to="+str(end_date)+""

    try:
        payload = nsefetch(url)["data"]
        return pd.DataFrame.from_records(payload)
    except:
        logging.error('Something went wrong')


def generate_payload_for_source(symbol, source):
    if source == 'NSE Official Website':
        df = generate_nse_payload_with_chuncks(symbol)
        df = df.drop(df.columns[[0, 1, 2, 3, 15, 16, 18, 19]], axis=1)
        return df
    elif source == 'Yahoo Finance':
        df = load_data_yf(symbol+'.NS')
        return df

def generate_payload_for_manual(symbol, source):
    if source == 'NSE Official Website':
        df = generate_nse_payload_with_chuncks(symbol)
        df = df.drop(df.columns[[0, 1, 2, 3, 15, 16, 18, 19]], axis=1)
        return df
    elif source == 'Yahoo Finance':
        df = load_data_yf(symbol+'.NS')
        return df




def generate_nse_payload_with_chuncks(symbol):

    start_date = START
    end_date = TODAY

    logging.info("Starting Date: "+str(start_date))
    logging.info("Ending Date: "+str(end_date))

    #We are calculating the difference between the days
    diff = end_date-start_date

    logging.info("Total Number of Days: "+str(diff.days))
    logging.info("Total FOR Loops in the program: "+str(int(diff.days/40)))
    logging.info("Remainder Loop: " + str(diff.days-(int(diff.days/40)*40)))

    total=pd.DataFrame()
    for i in range (0,int(diff.days/40)):

        temp_date = (start_date+ timedelta(days=(40))).strftime("%d-%m-%Y")
        start_date = datetime.strftime(start_date, "%d-%m-%Y")

        logging.info("Loop = "+str(i))
        logging.info("====")
        logging.info("Starting Date: "+str(start_date))
        logging.info("Ending Date: "+str(temp_date))
        logging.info("====")

        total=total.append(equity_history_virgin_nse(symbol,start_date,temp_date))

        logging.info("Length of the Table: "+ str(len(total)))

        #Preparation for the next loop
        start_date = datetime.strptime(temp_date, "%d-%m-%Y")


    start_date = datetime.strftime(start_date, "%d-%m-%Y")
    end_date = datetime.strftime(end_date, "%d-%m-%Y")

    logging.info("End Loop")
    logging.info("====")
    logging.info("Starting Date: "+str(start_date))
    logging.info("Ending Date: "+str(end_date))
    logging.info("====")

    total=total.append(equity_history_virgin_nse(symbol,start_date,end_date))

    logging.info("Finale")
    logging.info("Length of the Total Dataset: "+ str(len(total)))
    payload = total.iloc[::-1].reset_index(drop=True)
    return payload.sort_values(by=['TIMESTAMP']).reset_index(drop=True)

def load_data_yf(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data