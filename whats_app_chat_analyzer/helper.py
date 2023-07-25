from urlextract import URLExtract
from wordcloud import WordCloud
extract =URLExtract()
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    num_message = df.shape[0]
    words = []
    for message in df['messages']:
         words.extend(message.split())

    num_media_messages=df[df['messages'] =='<Media omitted>\n'].shape[0]

    Links =[]
    for message in df['messages']:
        Links.extend(extract.find_urls(message))

    return num_message, len(words), num_media_messages, len(Links)


def most_busy_user(df):
    temp = df[df['users'] != 'group_notification']
    x = temp['users'].value_counts()
    df =round((temp['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index': 'name', 'users': 'percent'})
    return x, df


def create_wordcloud(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc= wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]


    return df['day'].value_counts()