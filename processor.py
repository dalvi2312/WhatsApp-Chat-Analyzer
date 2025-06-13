import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    pattern = r"\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s?[ap]m\s-\s"

    message = re.split(pattern,data)[1:]
    date_time = re.findall(pattern,data)

    df = pd.DataFrame({'user_message':message , 'date_time': date_time})

    df['date_time'] = pd.to_datetime(df['date_time'].str.replace('\u202f', ' ', regex=True), format='%d/%m/%y, %I:%M %p - ')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if(entry[1:]):
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    df['date'] = df['date_time'].dt.date
    df['date'] = pd.to_datetime(df['date']) 
    df['day_name'] = df['date'].dt.day_name()

    df.drop(columns=['date_time'], inplace=True)
    df.drop(columns=['date'], inplace=True)
    return df



