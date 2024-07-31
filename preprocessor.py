import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:am|pm)\s-\s' #regular expression of date and time
    data = data.replace('\u202f', '')
    messages=re.split(pattern,data,flags=re.IGNORECASE)[1:]
    dates = re.findall(pattern,data,re.IGNORECASE)  # Use re.IGNORECASE to match 'am' and 'pm' case insensitively
    if len(messages) != len(dates):
        raise ValueError("The lengths of the messages and dates lists are not the same.")
    df=pd.DataFrame({'user_messages':messages,'Message_Date':dates})
    date_format = '%d/%m/%y, %I:%M%p - '
    df['Message_Date'] = pd.to_datetime(df['Message_Date'], format=date_format, errors='coerce') # 'coerce' parameter in the pd.to_datetime function tells Pandas to handle errors by converting any invalid parsing attempts into NaT (Not a Time).

    # Initialize empty lists to store the users and messages
    users = []
    messages = []
    # Iterate over each message in the 'user_messages' column
    for message in df['user_messages']:
        # Split the message into user and message using a regular expression
        entry = re.split(r'([\w\W]+?):\s', message,maxsplit=1)
        if len(entry) > 2:  # If the split result contains both user and message
            users.append(entry[1])  # Add the user to the users list
            messages.append(entry[2])  # Add the message to the messages list
        else:  # If it's a notification
            users.append('Group Notification')  # Add 'Group Notification' as the user
            messages.append(entry[0])  # Add the entire message to the messages list

        # Add the new columns to the DataFrame
    df['User'] = users
    df['Message'] = messages

    # Optionally drop the original 'user_messages' column
    df.drop(columns=['user_messages'], inplace=True)
    df['Year'] = df['Message_Date'].dt.year
    df['month_num']=df['Message_Date'].dt.month
    df['Month']=df['Message_Date'].dt.month_name()
    df['Day_name']=df['Message_Date'].dt.day_name()
    df['Day']=df['Message_Date'].dt.day
    df['Hour']=df['Message_Date'].dt.hour
    df['Message_Date'] = df['Message_Date'].dt.strftime('%d/%m/%y, %I:%M %p') 
    df.head(5)

    period=[]
    for hour in df[['Day_name','Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour)+'-'+str('00'))
        elif hour ==0:
            period.append(str('00')+'-'+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    df['Period']=period
    return df