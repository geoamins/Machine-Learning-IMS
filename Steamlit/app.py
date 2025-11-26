import streamlit as st
import pandas as pd
import random

st.title('Welcome to Guess a Number')
st.write('This is a simple web app where you can guess a number between 1 and 100.')

# Initialize the number to guess in session state
if 'number_to_guess' not in st.session_state:
    st.session_state.number_to_guess = random.randint(1, 100)

st.write(f'(For debugging purposes, the number to guess is: {st.session_state.number_to_guess})')
user_guess = int(st.number_input('Enter your guess:', min_value=1, max_value=100, step=1))

if user_guess == st.session_state.number_to_guess:
    st.success('You guessed correctly!')
    st.balloons()
elif user_guess < st.session_state.number_to_guess:
    st.info('Your guess is too low.')
else:
    st.info('Your guess is too high.')
