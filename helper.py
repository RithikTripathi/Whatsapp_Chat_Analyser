from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split(" "))

    # fetching number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetching number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def fetch_most_active_users(df):
    user_df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'User', 'user': 'Percent'})

    return df['user'].value_counts().head(), user_df_percent


def create_worldCloud(selected_user, df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wordcloud = wc.generate(df['message'].str.cat(sep=" "))
    return df_wordcloud


def most_common_words(selected_user, df):

    stopWFile = open('stop_hinglish.txt','r')
    stopWords = stopWFile.read()

    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group Notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopWords:
                words.append(word)

    most_common_df =  pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_analysis(selected_user, df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " - " + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    d_timeline = df.groupby('Date').count()['message'].reset_index()
    return d_timeline

def weekly_activity(selected_user, df) :
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity(selected_user, df) :
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df) :
    if selected_user != 'Overall Analysis':
        df = df[df['user'] == selected_user]

    details = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return details