import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload Chat File")
if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    # to convert the uploaded file data into string
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocessor(data)

    # to Display Dataframe
    st.dataframe(df) 

    # fetch unique users
    users = df['user'].unique().tolist()
    users.remove('Group Notification')
    users.sort()
    # option to go for overall analysis at 0th position
    users.insert(0, "Overall Analysis")

    selected_user = st.sidebar.selectbox("Show Analysis for ", users)

    if st.sidebar.button("Fetch Results"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

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
            timeline = helper.monthly_timeline(selected_user, df)

            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='Green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:

            # daily timeline
            st.subheader("Daily Chat Frequency")
            daily_timeline = helper.daily_timeline(selected_user, df)

            fig, ax = plt.subplots()
            ax.plot(daily_timeline['Date'], daily_timeline['message'], color='Black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # activity map

        st.subheader('Activity Tracker')
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Busiest Day Analysis')
            busy_day = helper.weekly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'Black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader('Busiest Month Analysis')
            busy_month = helper.monthly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = '#23395d')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # activity heatmap
        st.subheader("Weekly Activity Heatmap")
        details = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(details)
        st.pyplot(fig)

        # finding most active users in group
        if selected_user == "Overall Analysis":

            topUsers, topUsersPercent = helper.fetch_most_active_users(df)
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

            st.subheader('Most Used Words')
            df_worldCloud = helper.create_worldCloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_worldCloud)
            st.pyplot(fig)

            # most common words
            most_common_df = helper.most_common_words(selected_user, df)

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
            emoji_df = helper.emoji_analysis(selected_user, df)

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)





