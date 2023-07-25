import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    years = df['message_date'].dt.year
    df['year'] = years
    months = df['message_date'].dt.month_name()
    df['month'] = months
    df['month_num'] = df['message_date'].dt.month
    date = df['message_date'].dt.day
    df['day'] = df['message_date'].dt.day_name()
    df['date'] = date
    hours = df['message_date'].dt.hour
    minute = df['message_date'].dt.minute
    df['hour'] = hours
    df['minute'] = minute
    df.drop(columns=['message_date'], inplace=True)

    return df