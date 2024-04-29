import streamlit as st
from deta import Deta
import io
import docx
from streamlit_js_eval import streamlit_js_eval

def get_essay_list():
    # Logging into Deta.Space database
    DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
    deta = Deta(DETA_KEY)
    db = deta.Drive("Write_Your_Essay")

    # Getting the essay lists
    response = db.list()["names"]
    response.reverse()
    return response

def get_essay_from_name(essay_name):
    # Logging into Deta.Space database
    DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
    deta = Deta(DETA_KEY)
    db = deta.Drive("Write_Your_Essay")

    # Get the file from Deta.Space database
    file = db.get(essay_name)
    file_stream = io.BytesIO(file.read())
    return file_stream

def get_text_from_file(file_stream):
    doc = docx.Document(file_stream)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def remove_essay_from_name(essay_name):
    # Logging into Deta.Space database
    DETA_KEY = 'c0ki5D3avML_gSssDuj33rfuzLDrjwL1gc42oQkbgsHj'
    deta = Deta(DETA_KEY)
    db = deta.Drive("Write_Your_Essay")

    db.delete(essay_name)
    streamlit_js_eval(js_expressions="parent.window.location.reload()")
