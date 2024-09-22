import google.generativeai as genai
import streamlit as st
import time

# Google API configuration
GOOGLE_API_KEY = "AIzaSyAlojWi6VpcR6-kYhCwVAb2rw2U6J0lXco"
genai.configure(api_key=GOOGLE_API_KEY)

# Model Initialization
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get response from the model
def getResponseFromModel(user_input):
    response = model.generate_content(user_input)
    return response.text

# Streamlit configuration
st.set_page_config(page_title="Chatter", layout="centered")

# Set a refreshing background color
page_bg_style = """
<style>
    body {
        background-color: #f0f4f8;  /* Light refreshing color */
    }

    .bubble {
        border-radius: 10px;
        padding: 10px 15px;
        margin: 10px 0;
        max-width: 70%;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
        transition: background-color 0.3s;
    }

    .user-bubble {
        background-color: #A8C6FA;  /* User message color */
        color: black;
        text-align: right;
        float: right;
        clear: both;
    }

    .bot-bubble {
        background-color: #d1e7dd;  /* Bot response color */
        color: black;
        text-align: left;
        float: left;
        clear: both;
    }
</style>
"""
st.markdown(page_bg_style, unsafe_allow_html=True)

# Centered title
st.markdown("<h1 style='text-align: center; color: #4a4a4a;'>Chatter</h1>", unsafe_allow_html=True)
st.write("<h5 style='text-align: center; color: #6c757d;'>Powered by Gemini AI.</h5>", unsafe_allow_html=True)

# Initialize chat history in session state if not already initialized
if "history" not in st.session_state:
    st.session_state["history"] = []

# Function to handle message submission
def submit_message():
    user_input = st.session_state["user_input"]
    if user_input.strip() != "":  # Ensure non-empty messages
        # Show loading animation
        st.session_state["loading"] = True
        time.sleep(1)  # Simulate loading time
        
        # Get bot response
        response = getResponseFromModel(user_input)
        
        # Append user message and bot response to the chat history
        st.session_state.history.append((user_input, response))
        
        # Clear the input field after submission
        st.session_state["user_input"] = ""
        st.session_state["loading"] = False

# Display chat history in professional style bubbles
for user_message, bot_message in st.session_state.history:
    # User message (right-aligned)
    st.markdown(f"""
    <div class="bubble user-bubble">
        {user_message}
    </div>
    """, unsafe_allow_html=True)

    # Bot response (left-aligned)
    st.markdown(f"""
    <div class="bubble bot-bubble">
        {bot_message}
    </div>
    """, unsafe_allow_html=True)

    # Separate box for code responses (if applicable)
    if "```" in bot_message:  # Checks if the response contains code
        code_snippet = bot_message.split("```")[1]
        st.code(code_snippet, language='python')  # Assuming it's Python code, adjust as needed

# Clear float after chat bubbles to maintain alignment
st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

# Text input for user message, directly submits when 'Enter' is pressed
st.text_input("Type your message", key="user_input", on_change=submit_message)
