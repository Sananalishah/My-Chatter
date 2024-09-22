import google.generativeai as genai
import streamlit as st

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

# Set the background color of the whole app
page_bg_style = """
<style>
    body {
        background-color: #8da8a3;  /* Light sky blue background */
    }
</style>
"""
st.markdown(page_bg_style, unsafe_allow_html=True)

# Centered title
st.markdown("<h1 style='text-align: center; color: #a3e3d6;'>Chatter</h1>", unsafe_allow_html=True)
st.write("Powered by Gemini AI.")

# Initialize chat history in session state if not already initialized
if "history" not in st.session_state:
    st.session_state["history"] = []

# Function to handle message submission
def submit_message():
    user_input = st.session_state["user_input"]
    if user_input.strip() != "":  # Ensure non-empty messages
        # Get bot response
        response = getResponseFromModel(user_input)
        
        # Append user message and bot response to the chat history
        st.session_state.history.append((user_input, response))
        
        # Clear the input field after submission
        st.session_state["user_input"] = ""

# Display chat history in professional style bubbles
for user_message, bot_message in st.session_state.history:
    # User message (right-aligned, bluish-grey)
    st.markdown(f"""
    <div style="background-color: #A8C6FA; color: black; border-radius: 10px; padding: 10px 15px; 
                margin: 10px 0; max-width: 70%; text-align: right; float: right; 
                clear: both; box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);">
        {user_message}
    </div>
    """, unsafe_allow_html=True)

    # Bot response (left-aligned, attractive grey)
    st.markdown(f"""
    <div style="background-color: #b0b0b0; color: black; border-radius: 10px; padding: 10px 15px; 
                margin: 10px 0; max-width: 70%; text-align: left; float: left; 
                clear: both; box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);">
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
