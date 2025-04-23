# JARVIS Streamlit Version
import streamlit as st
import datetime
import threading
import speech_recognition as sr
import pyttsx3

# Initialize the Streamlit app
st.set_page_config(page_title="JARVIS AI Assistant", layout="wide")
st.markdown("<h1 style='text-align: center; color: #64ffda;'>JARVIS AI Assistant</h1>", unsafe_allow_html=True)

# State initialization
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'status' not in st.session_state:
    st.session_state.status = "Ready"
if 'expecting_code' not in st.session_state:
    st.session_state.expecting_code = False

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def add_to_conversation(sender, message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.conversation.append(f"[{timestamp}] {sender}: {message}")

def display_conversation():
    conversation_text = "\n".join(st.session_state.conversation)
    st.text_area("Conversation", conversation_text, height=400, disabled=True)

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.pause_threshold = 1
        add_to_conversation("JARVIS", "Listening for your command...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio, language="en-in")
            add_to_conversation("You (Voice)", query)
            return query
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand what you said."
        except sr.RequestError:
            return "Network error. Please check your connection."
        except Exception as e:
            return f"Error: {str(e)}"

def process_command(command):
    st.session_state.status = "Processing..."
    response = f"I received your command: {command}"
    add_to_conversation("JARVIS", response)
    st.session_state.status = "Ready"

def handle_code_input(code):
    add_to_conversation("JARVIS", "Processing your code...")
    # Placeholder logic for code correction
    corrected_code = code.replace("print", "# corrected: print")
    add_to_conversation("JARVIS", f"Corrected Code:\n{corrected_code}")

# Sidebar
st.sidebar.title("Controls")
input_mode = st.sidebar.radio("Input Mode", ["Text", "Voice"])

tab1, tab2 = st.tabs(["💬 Chat", "</> Code Correction"])

with tab1:
    display_conversation()

    user_input = ""
    if input_mode == "Text":
        user_input = st.text_input("Type your command")
        if st.button("Send"):
            if user_input:
                add_to_conversation("You", user_input)
                process_command(user_input)
    else:
        if st.button("🎤 Listen"):
            with st.spinner('Listening...'):
                query = take_command()
                add_to_conversation("JARVIS", query)
                process_command(query)

    st.text(f"Status: {st.session_state.status}")

with tab2:
    st.subheader("Submit your code for correction")
    code_input = st.text_area("Enter Code Here", height=300)
    if st.button("Submit Code"):
        if code_input.strip():
            handle_code_input(code_input)

st.sidebar.markdown("---")
st.sidebar.text("Status: " + st.session_state.status)

st.sidebar.button("Reset Conversation", on_click=lambda: st.session_state.update({'conversation': []}))
