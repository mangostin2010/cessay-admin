import streamlit as st
from dependencies import get_essay_list
import random

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

# Open Style Sheet and apply
with open('style.css', encoding='UTF-8') as f:
    st.html(f"<style>{f.read()}</style>")

if 'initialized' not in st.session_state:
    # Get essay list from dependencies.py
    st.session_state.essay_list = get_essay_list()
    st.session_state.initialized = True

essay_list = st.session_state.essay_list

st.title('Check Student\'s Essay')
st.divider()

a_style = """color: rgb(49, 51, 63);display: block ruby; text-align: center; text-decoration: none; font-size: 16px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);"""

for x in essay_list:
    URL_STRING = f"check-cessay.streamlit.app/check?target={x}"
    #URL_STRING = f"http://127.0.0.1:8501/check?target={x}"
    x_placeholder = x.replace('.docx', '')
    
    # Define a button for each essay
    st.markdown(
        f'<a href="{URL_STRING}" style="{a_style}" target="_self">{x_placeholder}</a>',
        unsafe_allow_html=True
    )

# Removing everything in st.session_state dictionary
for x in st.session_state:
    del st.session_state[x]
