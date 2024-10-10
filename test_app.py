import streamlit as st

print('Streamlit Modulpfad:', st.__file__)
print('experimental_rerun' in dir(st))

st.write('Streamlit Version:', st.__version__)

if st.button('Rerun'):
    st.experimental_rerun()
