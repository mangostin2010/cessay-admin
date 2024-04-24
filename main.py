from streamlit_js_eval import streamlit_js_eval
import docx
from deta import Deta
import streamlit as st
import io
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

with open('style.css', encoding='UTF-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if 'db' not in st.session_state:
    DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
    deta = Deta(DETA_KEY)
    db = deta.Drive("Write_Your_Essay")
    st.session_state.db = db

if 'response_list' not in st.session_state:
    response = st.session_state.db.list()["names"]
    response.reverse()
    st.session_state.response_list = response

if 'download' not in st.session_state:
    st.session_state.download = False

st.title('Check Student\'s Essay')
st.divider()

st.session_state.response_list


code = """
<style>
button {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
"""
st.html(code)

for x in st.session_state.response_list:
    if st.button(label=x.replace('.docx', ''), use_container_width=1):
        streamlit_js_eval(js_expressions='location.href = "http://example.com";')
    #st.link_button(label=x.replace('.docx', ''), use_container_width=1, url=f"https://check-cessay.streamlit.app/check_essay?target={x}")
