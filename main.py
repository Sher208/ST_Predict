from components.dashboard import body
import streamlit as st


if __name__ == "__main__":
    try:
        body()
    except KeyError:
        st.error('Missing input')