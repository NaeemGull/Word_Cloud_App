import streamlit as st
import pandas as pd
import numpy as np
# import mymodel as m


# Adding title of your page 
st.title("My First App")

# Adding Simple Text 
st.write("Hello World!")

st.write("""
    My First App in Python using Streamlit.....
""")

# User Input 
number = st.slider('Pick a number : ', 0, 100, 25)

# Print the User Input
st.write(f"You Selected Number : {number}")

# Adding a button
if st.button('Greeting '):
    st.write('Hey, Hello Dear')
else:
    st.write("Good-bye")

# Adding radio button with option

genre = st.radio(
    "What's your favorite movie genre",
    ("Comedy", "Drama", "Documentary", "Action")
)

st.write(f"Your Favorite movie : {genre}")


# Adding a Drop Draw List

# option = st.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Phone Number", "Home Phone Number")
# )

# st.write(f"Your Contact option : {option}")

# Adding a drop draw list on the sidebar

option = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Phone Number", "Home Phone Number")
)


# Add your whatApp Number
st.sidebar.text_input("Enter your whatsapp number")

# Add a file uploader
uploader_file = st.sidebar.file_uploader(
    "choose a CSV", type="CSV"
)


#  Creat a line plot 
# ploting
data = pd.DataFrame({
    'first column': list(range(1, 11)),
    'Second column': np.arange(number, number + 10) 
})
st.line_chart(data)

















st.write("""
# Sales Model
Below are our sales predictions
for this customer.

# Naeem

""")

# st.write(m.run(window+15))











