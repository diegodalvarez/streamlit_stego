import streamlit as st
from stego_base import * 

st.header("PNG Stegongraphy")
with st.beta_expander('purpose'):
    st.write("Least Significant Bit steganography for PNG see github for source. Each option saves a file for, example if you want to decode you have select the encoded file")

data = st.file_uploader("Upload a PNG", type=["png"])

if data is not None:
    
    option = st.selectbox("select option", ("encode", "decode"))
    
    if option == "encode":
        
        message = st.text_input("put message in here")
        
        run = st.radio("select run once ready", ("stop", "run"))
        
        if run == "run":
    
            image = Stego(data, message)
            test = image.Encode()
        
    if option == "decode":    
        
        image = Stego(data, 0)
        test = image.Decode()
    
st.write('Created by Diego Alvarez for CYBR 5330')
