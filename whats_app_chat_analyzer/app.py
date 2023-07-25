import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp Chat Analyzer")


uploaded_file =st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    st.dataframe(df)


    # Unique User
    Users5 =df['users'].unique().tolist()
    Users5.sort()
    Users5.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", Users5)

    if st.sidebar.button("Show Analysis"):

        num_message, words, num_media_messages, num_links =helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_message)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links shared")
            st.title(num_links)

        #timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['messages'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='red')
            st.pyplot(fig)









        # finding the busiest users in the group(group level)
        if selected_user =='Overall':
            st.title('Most busy Users')
            x, new_df =helper.most_busy_user(df)
            fig, ax =plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig, ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.2f")
            st.pyplot(fig)