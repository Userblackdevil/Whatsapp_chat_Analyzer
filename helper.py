from urlextract import URLExtract
extractor=URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import seaborn as sns
def fetch_stats(selected_user,df):
    if selected_user!='OverAll':
       df=df[df['User']==selected_user]

    num_message=df.shape[0]
    words=[]
    messages=[]
    for message in df['Message']:
        words.extend(message.split())
        messages.append(message)
    media=df[df['Message']=='<Media omitted>\n'].shape[0]

    links=[]
    for link in df['Message']:
        links.extend(extractor.find_urls(link))    
    return num_message,len(words), messages,media,len(links)
def fetch_most_busyUser(df):
    x=df['User'].value_counts().head()
    df=round((df['User'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'Name','count':'Percentage'})
    return x,df
def create_wordcloud(selected_user,df):
    if selected_user!='OverAll':
       df=df[df['User']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='White')
    df_wc=wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc
def most_comman_word(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='OverAll':
       df=df[df['User']==selected_user]
    temp=df[df['User']!='Group Notification']
    temp=temp[temp['Message']!='<Media omitted>\n']

    words=[]
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return_df=pd.DataFrame(Counter(words).most_common(20))
    return return_df
# def emoji(selected_user,df):
#     if selected_user!='OverAll':
#         df=df[df['User']==selected_user]
#     emojis=[]
#     emoji_set = set(emoji.EMOJI_DATA.keys())
#     for message in df['Message']:
#         # emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI('en')])
#         # emojis.extend([c for c in message if c in emoji_set])
#         emoji_set = set(emoji.UNICODE_EMOJI['en'].keys())
#         emojis.extend(emoji_set)
#     emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df
def emoji_count(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['User'] == selected_user]
    
    emojis = []
    
    for message in df['Message']:
        for char in message:
            if emoji.is_emoji(char):
                emojis.append(char)
    
    # Count occurrences of each emoji
    emoji_counter = Counter(emojis)
    
    # Convert Counter to DataFrame
    emoji_df = pd.DataFrame(emoji_counter.items(), columns=['Emoji', 'Count'])
    
    # Sort DataFrame by Count in descending order
    emoji_df = emoji_df.sort_values(by='Count', ascending=False).reset_index(drop=True)
    
    return emoji_df
def monthly_timeline(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['User'] == selected_user]
    timeline=df.groupby(['Year','month_num','Month']).count()['Message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i]+'-'+str(timeline['Year'][i]))
    timeline['Time']=time
    return timeline
def Day(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['User'] == selected_user]
    return df['Day_name'].value_counts()
def month(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['User'] == selected_user]
    return df['Month'].value_counts()
def Activity_heatmap(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['User'] == selected_user]
    user_heatmap=df.pivot_table(index='Day_name',columns='Period',values='Message',aggfunc='count').fillna(0)
    return user_heatmap
    

