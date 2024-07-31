import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import preprocessor,helper
import base64


def add_local_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
# Path to your local background image
background_image_path = 'pic2.jpg'

# Add background image
add_local_background_image(background_image_path)
st.sidebar.image('pic1.jpg')
st.sidebar.title('WhatsApp Chat Analyzer')
uploaded_file =st.sidebar.file_uploader('Choose a File')
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)

    # st.dataframe(df)
    unique_user=df['User'].unique().tolist()
    unique_user.remove('Group Notification')
    unique_user.sort()
    unique_user.insert(0,'OverAll')
    selected_user=st.sidebar.selectbox('Show Analysis for users',unique_user)

if st.sidebar.button('Show Analysis'):
    num_message,words,Message,media,links=helper.fetch_stats(selected_user,df)
    st.title('Top Statsitics')
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.header('Total Message')
        st.title(num_message)
    with col2:
        st.header('Total Words')
        st.title(words)
    st.title('Message done by'+' '+selected_user)
    st.dataframe(Message)  
    with col3:
        st.header('Media Shared by'+' '+selected_user)
        st.title(media)
    with col4:
        st.header('Links Shared by the'+' '+selected_user)
        st.title(links)
    st.title('Monthly Timeline')
    time=helper.monthly_timeline(selected_user,df)
    fig,ax=plt.subplots()
    ax.plot(time['Time'],time['Message'],color='Green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    if selected_user=='OverAll':
        st.title('Most Active Users')
        x,new_df = helper.fetch_most_busyUser(df)
        fig , ax =plt.subplots()
        col1,col2=st.columns(2)
        with col1:
            ax.bar(x.index,x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)
    st.title('WordCloud')
    df_wc=helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    comman_word=helper.most_comman_word(selected_user,df)
    st.title('Most Comman words Used by'+' '+selected_user)
    fig ,ax=plt.subplots()
    ax.bar(comman_word[0],comman_word[1],color=["#ffaa00", "black", 'red'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    Comman_Emoji=helper.emoji_count(selected_user,df)
    st.title('Most Used Emojis')
    st.dataframe(Comman_Emoji)
    st.title('Activity Map')
    col1,col2=st.columns(2)
    with col1:
        st.header('Most Busy Day')
        Day=helper.Day(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(Day.index,Day.values)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    with col2:
        st.header('Most Busy Month')
        Month=helper.month(selected_user,df)
        fig,ax=plt.subplots()
        ax.bar(Month.index,Month.values,color='Orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title('Weekly Activity Map')
    user_heatmap=helper.Activity_heatmap(selected_user,df)
    fig,ax=plt.subplots(figsize=(30,30))
    ax=sns.heatmap(user_heatmap,annot=True)
    st.pyplot(fig)