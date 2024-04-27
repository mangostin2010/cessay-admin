from streamlit_js_eval import streamlit_js_eval
import docx
from deta import Deta
import streamlit as st
import io
import time

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

with open('style.css', encoding='UTF-8') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#if 'target' not in st.query_params:
#    st.switch_page('main.py')
#else:
#    st.query_params.target = st.query_params['target']
try:
    st.session_state.target = st.query_params["target"]
except:
    st.switch_page('main.py')
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
    file_stream = io.BytesIO(file.read())

    st.download_button(label=f"**Download :blue[{st.session_state.target}]**",
                    data=file_stream,
                    file_name=st.session_state.target,
                    mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    st.session_state.file_downloaded = True

preview = st.expander('Preview this essay')

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

for key in st.session_state:
    del st.session_state[key]
st.query_params.clear()
st.session_state
streamlit_js_eval(js_expressions="history.back();")
