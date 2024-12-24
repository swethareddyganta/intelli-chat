import streamlit as st
from transformers import pipeline
import general_conv
from getanswer import execute_query
import pandas as pd
from Summarizer import query_document

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define the labels
labels = ["health medical", "general conversation", 'education study']

# Initialize session state for conversation and analytics
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = ""
if "analytics" not in st.session_state:
    st.session_state.analytics = {"general conversation": 0, "other conversations": 0}
if "last_classification_result" not in st.session_state:
    st.session_state.last_classification_result = ""
if "last_document_id" not in st.session_state:
    st.session_state.last_document_id = ""

# App layout
st.title("Wikipedia small language model")

# Create tabs
tab1, tab2 = st.tabs(["Chat", "Analytics"])

# Tab 1: Chat Interface
with tab1:
    # User input
    user_input = st.text_input("Your Message:", placeholder="Type your message here...")
    
    # Generate response and update conversation
    if st.button("Chitchat"):
        if user_input.strip():
            st.session_state.conversation_history += f"\n<b><span style='font-size:20px;'>User: {user_input}</span></b>\n"
            
            st.session_state.analytics["general conversation"] += 1
            st.session_state.last_classification_result = general_conv.main(user_input)
            st.session_state.last_document_id = 'general conv'
            
            # Add classification result to conversation history
            st.session_state.conversation_history += f"\n{st.session_state.last_classification_result}\ndocument_id:{st.session_state.last_document_id}\n"
            
            # Clear the input box
            st.session_state["user_input"] = ""
            st.rerun()

    if st.button("Topic Question"):
        if user_input.strip():
            st.session_state.conversation_history += f"\n<b><span style='font-size:20px;'>User: {user_input}</span></b>\n"
            
            st.session_state.analytics["other conversations"] += 1
            query = [user_input]
            result, document_id = execute_query(query)
            
            final_doc = ''
            for doc in result:
                final_doc = final_doc + doc
            
            st.session_state.last_classification_result = query_document(final_doc, query[0])
            st.session_state.last_document_id = document_id
            
            # Add classification result to conversation history
            st.session_state.conversation_history += f"\n{st.session_state.last_classification_result}\ndocument_id:{st.session_state.last_document_id}\n"
            
            # Clear the input box
            st.session_state["user_input"] = ""
            st.rerun()

    # Display conversation history
    st.markdown(st.session_state.conversation_history, unsafe_allow_html=True)

# Tab 2: Analytics
with tab2:
    st.header("Conversation Analytics")
    analytics_data = st.session_state.analytics

    df = pd.DataFrame(list(analytics_data.items()), columns=['Category', 'Count'])
    st.bar_chart(df.set_index('Category'))