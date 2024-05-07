import streamlit as st

with open('style.css', encoding='UTF-8') as f:
  st.html(f'<style>{f.read()}</style>')
st.info('Cessay의 공식 페이지가 이전 되었습니다!🎉 이제부터는 불편한 하단 Streamlit버튼 없이 Cessay를 이용할 수 있으며 뒤로가기 버튼이 작동하오니 다음 링크를 사용해주세요.')
st.page_link("http://check-cessay.kro.kr", label="check-cessay.kro.kr", icon="📄")
st.page_link("http://cessay.kro.kr", label="cessay.kro.kr", icon="✏️")
