import streamlit as st

st.title("Exercise: State Management")

st.subheader("Temperature conversion")

# Initialize state with temperatures.
# Use the freezing point of water
if 'celsius' not in st.session_state:
    st.session_state['celsius'] = 0.0
if 'fahrenheit' not in st.session_state:
    st.session_state['fahrenheit'] = 32.0
if 'kelvin' not in st.session_state:
    st.session_state['kelvin'] = 273.15

# Write a callback to convert the temperature in Celsius
# to Farenheit and Kelvin. Change the values in the state
# appropriately
def c_update():
    celsius = st.session_state['celsius']
    st.session_state['fahrenheit'] = (celsius * 1.8) + 32
    st.session_state['kelvin'] = celsius + 273.15

# Same thing, but converting from Farenheit to Celsius
# and Kelvin
def f_update():
    fahrenheit = st.session_state['fahrenheit']
    st.session_state['celsius'] = (fahrenheit - 32) / 1.8
    st.session_state['kelvin'] = (fahrenheit + 459.67) / 1.8

# Same thing, but converting from Kelvin to Celsius
# and Farenheint
def k_update():
    kelvin = st.session_state['kelvin']
    st.session_state['celsius'] = kelvin - 273.15
    st.session_state['fahrenheit'] = kelvin * 1.8 - 459.67

# Write a callback that adds whatever number the user
# inputs to the Celsius box. Use args.
def add_celsius(deg):
    st.session_state['celsius'] += deg
    c_update()

# Write a callback to sets the temperatures depending on
# which button the user clicks. Use kwargs.
def set_temp(c=None, f=None, k=None):
    if c is not None:
        st.session_state['celsius'] = c
        c_update()
    elif f is not None:
        st.session_state['fahrenheit'] = f
        f_update()
    elif k is not None:
        st.session_state['kelvin'] = k
        k_update()

col1, col2, col3 = st.columns(3)

# Hook up the first 3 callbacks to the input widgets
col1.number_input("Celsius", step=0.01, key="celsius", on_change=c_update)
col2.number_input("Fahrenheit", step=0.01, key="fahrenheit", on_change=f_update)
col3.number_input("Kelvin", step=0.01, key="kelvin", on_change=k_update)

# Hook up the 4th callback to the button. Use args.
col1, _, _ = st.columns(3)
num = col1.number_input("Add to Celsius", step=1)
col1.button("Add", type="primary", on_click=add_celsius, args=[num])

col1, col2, col3 = st.columns(3)

# Hook up the last callback to each button. Use kwargs.
col1.button('🧊 Freezing point of water', on_click=set_temp, kwargs={'c': 0})
col2.button('🔥 Boiling point of water', on_click=set_temp, kwargs={'c': 100})
col3.button('🥶 Absolute zero', on_click=set_temp, kwargs={'k': 0})

st.write(st.session_state)