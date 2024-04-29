import streamlit as st
from dependencies import get_essay_from_name, get_text_from_file, remove_essay_from_name

st.set_page_config(page_title='Check Student\'s Essay', page_icon='✏️')

# Open Style Sheet and apply
with open('style.css', encoding='UTF-8') as f:
    st.html(f"<style>{f.read()}</style>")

# Checking whether user has target variable. If not, 
if 'target' not in st.session_state:
    st.switch_page('main.py')

def do_all():
    st.title('Check Student\'s Essay')
    st.divider()

    st.download_button(label=f"**Download :blue[{st.session_state.target}]**",
                    data=get_essay_from_name(st.session_state.target),
                    file_name=st.session_state.target,
                    mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')



    preview = st.expander('Preview this essay')

    delete_popover = st.popover("**:red[Delete This Essay]**")
    with delete_popover:
        agree = st.checkbox(':red[I understand this essay cannot be restored after being deleted.]')
            
        delete_button = st.button('**:red[Delete]**', disabled=not agree)
        if delete_button: remove_essay_from_name(st.session_state.target)

    if st.button('Go Back to Main Page'):
        st.switch_page('main.py')

    if 'preview_loaded' not in st.session_state:
        with preview:
            with st.spinner('Wait for it...'):
                st.session_state.preview_content = get_text_from_file(get_essay_from_name(st.session_state.target))

    with preview:
        file_content = st.session_state.preview_content
        file_name = st.session_state.target.replace('.docx','')
        divided_file_name = file_name.split('_')

        date = divided_file_name[0]
        name = divided_file_name[1]
        topic = divided_file_name[2]

        f'''### **:gray[{topic}]**'''
        
        # Write Content
        st.write(file_content.replace(date, '', 1).replace(name, '', 1).replace(',','',1).replace(topic, '', 1))
        st.session_state.preview_loaded = True

do_all()
