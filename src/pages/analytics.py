import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

if 'analytics' not in st.session_state:
    st.session_state.analytics = {'General Conversation':0,'Health':0, 
                                  'Education':0, 'Food':0, 'Sports':0,'Travel':0,
                                  'Entertainment':0,'Politics':0,'Economy':0,
                                  'Enviornment':0,'Technology':0,'Multi topic':0}
if 'query_timings' not in st.session_state:
        st.session_state.query_timings = {}

with st.sidebar:
    if st.button("Back to chat"):
        st.switch_page("Chat.py")

df = pd.DataFrame(list(st.session_state.analytics.items()), columns=['Category', 'Count']) # Plot the bar graph
# Bar chart
print(df)
st.title("Questions asked on different Topics")
st.bar_chart(df.set_index('Category'))

# Pie chart

def plot_pie_chart(data = st.session_state.analytics, main_key = 'General Conversation'):
    # print(st.session_state.analytics)
    # st.write(st.session_state.analytics)
    # Grouping all keys except the main_key into "Others"
    grouped_data = {main_key: data[main_key]}
    grouped_data['Topic Conversation'] = sum(value for key, value in data.items() if key != main_key)
    
    
    df = pd.DataFrame.from_dict(grouped_data, orient='index', columns=['Value'])
    df.index.name = 'Category'
    df.reset_index(inplace=True)
        # Create Streamlit app
    st.title('Chit chat and topic distribution')
    colors = ['#63b59d', '#aec7e8'] 
    # Create pie chart using Plotly Express
    fig = px.pie(df, values='Value', names='Category', 
                 title='Breakdown of Conversation Types',
                 color_discrete_sequence=colors)
    
    # Display the pie chart
    st.plotly_chart(fig)

def line_chart(data = st.session_state.query_timings):
    df = pd.DataFrame(list(data.items()), columns=['time', 'Count'])
    df = df.sort_values('time')
    print(df)
    st.title('Queries asked every second')
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df['Count'], marker='o')
    plt.title('Query Count by Time')
    plt.xlabel('Time of Day')
    plt.ylabel('Number of Queries')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Display the chart in Streamlit
    st.pyplot(plt) 
    



# Plot pie chart with 'a' as the main category
plot_pie_chart()
line_chart()

