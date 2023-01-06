import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from Analyser.util import preprocess
from Analyser.component.statistics import stats
from Analyser.component.timeline import timeline
from Analyser.component.activity import activity
from Analyser.component.wordCloud import worldCloud
from Analyser.component.commonWords import commonWords
from Analyser.component.emojii import emojii
from Analyser.constant import *

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload Chat File")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # to convert the uploaded file data into string
    data = bytes_data.decode("utf-8")

    preproc = preprocess(data= data)

    df = preproc.preprocessor()

    # to Display Dataframe
    st.dataframe(df) 

    # fetch unique users
    users = df[USER_COLUMN_HEADER_KEY].unique().tolist()
    users.remove('Group Notification')
    users.sort()
    # option to go for overall analysis at 0th position
    users.insert(0, OVERALL_ANALYSIS_KEY)

    selected_user = st.sidebar.selectbox("Show Analysis for ", users)

    if st.sidebar.button(FETCH_RESULTS_KEY):

        stats = stats(selected_user = selected_user, df = df)

        num_messages, words, num_media_messages, num_links = stats.fetch_stats()

        st.subheader("Whastapp Chat Analysis")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.title(num_messages)
        with col2:
            st.subheader("Total Words")
            st.title(words)
        with col3:
            st.subheader("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.subheader("Links Shared")
            st.title(num_links)


        # timeline

        col1, col2 = st.columns(2)

        with col1:
            # monthly timeline
            st.subheader('Monthly Chat Frequency')

            tl = timeline(selected_user= selected_user, df= df)
            timeline = tl.monthly_timleine()

            fig, ax = plt.subplots()
            ax.plot(timeline[TIME_KEY], timeline[MESSAGE_COLUMN_HEADER_KEY], color='Green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:

            # daily timeline
            st.subheader("Daily Chat Frequency")

            daily_timeline = tl.daily_timleine()

            fig, ax = plt.subplots()
            ax.plot(daily_timeline[DATE_HEADER_KEY], daily_timeline[MESSAGE_COLUMN_HEADER_KEY], color='Black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # activity map

        st.subheader('Activity Tracker')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Busiest Day Analysis')

            at = activity(selected_user= selected_user, df= df)
            busy_day = at.weekly_activity()

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'Black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader('Busiest Month Analysis')

            busy_month = at.monthly_activity()

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = '#23395d')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        # activity heatmap
        st.subheader("Weekly Activity Heatmap")

        details = at.activity_heatmap()

        fig, ax = plt.subplots()
        ax = sns.heatmap(details)
        st.pyplot(fig)


        # -----------------

        # finding most active users in group
        if selected_user == "Overall Analysis":

            topUsers, topUsersPercent = stats.fetch_most_active_user()
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Most Active Users")
                ax.bar(topUsers.index, topUsers.values, color="grey")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.subheader("Users Contribution")
                st.dataframe(topUsersPercent)


        # word cloud

        wc = worldCloud(selected_user= selected_user, df= df)

        st.subheader('Most Used Words')

        df_worldCloud = wc.create_worldCloud()

        fig, ax = plt.subplots()
        ax.imshow(df_worldCloud)
        st.pyplot(fig)


        # most common words

        cw = commonWords(selected_user= selected_user, df= df)

        most_common_df = cw.most_common_words()

        st.subheader('Frequently Used Words')

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_df)
        with col2:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1], color = '#23395d')
            st.pyplot(fig)
            plt.xticks(rotation = 'vertical')




        # emoji analysis

        st.subheader("Emoji Analysis")

        emoji = emojii(selected_user= selected_user, df= df)

        emoji_df = emoji.emoji_analysis()

        df_status = emoji_df.empty

        if df_status == True:
            st.write(f"No Emojis Send By User : {selected_user}")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)