from streamlit_js_eval import streamlit_js_eval
import docx
from deta import Deta
import streamlit as st
import io
import time
import os
from streamlit_cookies_manager import EncryptedCookieManager
import ast

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

cookies = EncryptedCookieManager(
    # This prefix will get added to all your cookie names.
    # This way you can run your app on Streamlit Cloud without cookie name clashes with other apps.
    prefix="justin",
    # You should really setup a long COOKIES_PASSWORD secret if you're running on Streamlit Cloud.
    password=os.environ.get("COOKIES_PASSWORD", "justin is handsome"),
)
if not cookies.ready():
    # Wait for the component to load and send us current cookies.
    st.stop()

st.write("Current cookies:", cookies)

def get_target_from_cookies(cookie_value):
    # Extract the dictionary part from the string
    start_index = str(cookie_value).find('{')
    end_index = str(cookie_value).rfind('}') + 1
    dict_string = str(cookie_value)[start_index:end_index]
    # Convert the string representation of dictionary to an actual dictionary
    cookie_dict = ast.literal_eval(dict_string)
    # Get the value of the 'asdf' key
    asdf_value = cookie_dict.get('asdf')
    return asdf_value

st.session_state.target = get_target_from_cookies(cookies)
st.session_state.target

with open('style.css', encoding='UTF-8') as f:
    st.html(f'<style>{f.read()}</style>')

if 'db' not in st.session_state:
    DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
    deta = Deta(DETA_KEY)
    db = deta.Drive("Write_Your_Essay")
    st.session_state.db = db
db = st.session_state.db

st.title('Check Student\'s Essay')
st.divider()

if 'file_downloaded' not in st.session_state:
    file = db.get(st.session_state.target)
    st.session_state.file_stream = io.BytesIO(file.read())
    st.session_state.file_downloaded = True

st.download_button(label=f"**Download :blue[{st.session_state.target}]**",
                data=st.session_state.file_stream,
                file_name=st.session_state.target,
                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    

preview = st.expander('Preview this essay')

def do_preview():
    with preview:
        # st.warning('⚠️ This process is still in developing.')
        def getText(file_stream):
            doc = docx.Document(file_stream)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            return '\n'.join(fullText)
    
        # Preview Expander
        file_content = getText(file_stream)
        file_name = st.session_state.target.replace('.docx','')
        divided_file_name = file_name.split('_')
    
        # Preview Datas
        date = divided_file_name[0]
        name = divided_file_name[1]
        topic = divided_file_name[2]
    
        f'''### **:gray[{topic}]**'''
        
        # Write Content
        st.write(file_content.replace(date, '', 1).replace(name, '', 1).replace(',','',1).replace(topic, '', 1))
    
with st.popover("**:red[Delete This Essay]**"):
    agree = st.checkbox(':red[I understand this essay cannot be restored after being deleted.]')
    if agree == False: st.session_state.understand = True
    elif agree == True: st.session_state.understand = False
        
    if st.button('**:red[Delete]**', disabled=st.session_state.understand):
        db.delete(st.session_state.target)
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

if st.button('Go Back to Main Page'): 
    st.switch_page('main.py')

del st.session_state["file_downloaded"]
