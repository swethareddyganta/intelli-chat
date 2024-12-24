from openai import OpenAI
import os
import shelve
import streamlit as st
from transformers import pipeline
import general_conv
from getanswer import execute_query
import pandas as pd
from Summarizer import query_document
import matplotlib.pyplot as plt
from datetime import datetime
from classifier import topic


st.title("Wikipedia Small Language Model")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"




def analytics(data_dict): # Convert the dictionary to a DataFrame 
    df = pd.DataFrame(list(data_dict.items()), columns=['Category', 'Count']) # Plot the bar graph
    print(df)
    st.title("Analytics")
    st.bar_chart(df.set_index('Category'))

def display_analytics():
    analytics(st.session_state.analytics)
    

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])


# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

if 'query_timings' not in st.session_state:
        st.session_state.query_timings = {}

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

if 'analytics' not in st.session_state:
    st.session_state.analytics = {'General Conversation':0,'Health':0, 
                                  'Education':0, 'Food':0, 'Sports':0,'Travel':0,
                                  'Entertainment':0,'Politics':0,'Economy':0,
                                  'Enviornment':0,'Technology':0,'Multi topic':0}

# Sidebar with a button to delete chat history
with st.sidebar:
    selected_form = st.selectbox(
    'Choose a form type:',
    ['General Conversation','Self-Operating Classifier','Multi Topic(Bonus)','Health', 'Education', 'Food', 'Sports','Entertainment','Politics','Economy','Technology','Environment','Travel']
)
    # print(selected_form)
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])
    if st.button("Analytics"):
        st.switch_page("pages/analytics.py")

print(selected_form)

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface
# Main chat interface
if prompt := st.chat_input("How can I help?"):

    if selected_form == 'Self-Operating Classifier':
        try:
            selected_form = topic(prompt)
        except Exception as e:
            selected_form = 'Health'
            print(f'e:{e}')
    current_hour = datetime.now().strftime("%H:%M:%S")
    print(selected_form)
    if 'query_timings' not in st.session_state:
        st.session_state.query_timings = {}
    st.session_state.query_timings[current_hour] = st.session_state.query_timings.get(current_hour,0) + 1

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.analytics[selected_form] = st.session_state.analytics.get(selected_form,0) + 1


    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        
        # Determine which function to use based on the condition
        if selected_form == 'General Conversation':
            # Use general_conv.main() for responses when k is less than 2
            print('sending to general Conversation')
            try:
                response = general_conv.main(prompt)
            except Exception as e:
                response = 'This query cant be handle now but will soon add it'
            document_id = 'General Conversation'
        else:
            query = [prompt]
            try:
                result,document_id = execute_query(query)
            except Exception as e:
                result = 'This query cant be handle now but will soon add it'
                document_id = 000
            final_doc = ''
            for doc in result:
                final_doc = final_doc + doc
            try:
                response =  query_document(final_doc[:16380], query[0])
            except Exception as e:
                response = 'This query cant be handle now but will soon add it'
        
        full_response = response + "\n" + 'document_id:' + str(document_id)
        # Display the full response
        message_placeholder.markdown(full_response)
    
    # Add the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)

