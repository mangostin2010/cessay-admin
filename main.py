from deta import Deta
import streamlit as st
import os
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

cookies = EncryptedCookieManager(
    # This prefix will get added to all your cookie names.
    # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
    prefix="justin",
    password=os.environ.get("COOKIES_PASSWORD", "justin is handsome"),
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.stop()

st.write("Current cookies:", cookies)

with open('style.css', encoding='UTF-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.query_params.clear()

if 'db' not in st.session_state:
    DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
    deta = Deta(DETA_KEY)
    db = deta.Drive("Write_Your_Essay")
    st.session_state.db = db

if 'response_list' not in st.session_state:
    response = st.session_state.db.list()["names"]
    response.reverse()
    st.session_state.response_list = response

st.title('Check Student\'s Essay')
st.divider()

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
        for key in st.session_state:
            del st.session_state[key]
        cookies['asdf'] = x
        if st.button('really?'):
            cookies.save()
            st.switch_page('pages/check_essay.py')
