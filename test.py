import streamlit as st
import pyarrow as pa

st.write("PyArrow is working!")
array = pa.array([1, 2, 3])
st.write(array)
