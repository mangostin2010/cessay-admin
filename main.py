from deta import Deta
import streamlit as st

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

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

        st.query_params.target = x
        st.switch_page('pages/check_essay.py')
