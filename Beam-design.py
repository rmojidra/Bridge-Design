import streamlit as st

st.set_page_config(page_title="Bridge Calc App", layout="wide")

st.title("Bridge Calculation App")

st.write("This is the first working version.")

st.header("Bent Cap Flexural Check")

fc = st.number_input("Concrete strength, f'c (ksi)", value=4.0)
fy = st.number_input("Steel yield strength, fy (ksi)", value=68.0)
b = st.number_input("Width, b (in)", value=60.0)
h = st.number_input("Height, h (in)", value=60.0)
cover = st.number_input("Cover (in)", value=2.0)
Mu = st.number_input("Factored moment, Mu (kip-ft)", value=8250.0)

st.success("Inputs are working.")
