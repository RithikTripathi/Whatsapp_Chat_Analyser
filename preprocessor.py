import re # for regex
import pandas as pd


def preprocessor(data):

    pattern = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s+\wm\s-\s'
    # to catch the regex expression of messages


    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separatinng user and message
    users = []
    messages = []
    for message in df['user_message']:
        record = re.split('([\w\W]+?):\s', message)
        if record[1:]:  # user name:
            users.append(record[1])
            messages.append(record[2])
        else:
            users.append('Group Notification')
            messages.append(record[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['Date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
