import streamlit as st
import processor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import emoji

st.sidebar.title("WhatsApp Chat Analayzier")
file = st.sidebar.file_uploader("Choose File")

if file is not None:
    byte_data = file.getvalue()
    data = byte_data.decode("utf-8")
    df = processor.preprocess(data)
    # st.dataframe(df)
    user_option = ['All'] + df['users'].unique().tolist()
    user_option.sort()
    selected_user = st.sidebar.selectbox("Choose a user", user_option)
    st.sidebar.write("You selected:", selected_user)

    #All Users

    if selected_user == 'All':
        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        total_messages = len(df['messages'])
        total_words = df['messages'].str.split().str.len().sum()
        media_files = df['messages'].str.contains("<Media omitted>").sum()
        with col1:
            st.header("Total Messages")
            st.header(total_messages)

        with col2:
            st.header("Total Words")
            st.header(total_words)

        with col3:
            st.header("Media Shared")
            st.header(media_files)
        
        st.title("📈Monthly Timeline")
        monthly = df.groupby(['month'])["messages"].count().to_frame().reset_index()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        monthly['month'] = pd.Categorical(monthly['month'], categories=month_order, ordered=True)
        monthly = monthly.sort_values('month')
        fig, ax = plt.subplots()
        sns.lineplot(data=monthly, x='month', y='messages', ax=ax)
        ax.tick_params(axis='x', rotation=45)
        ax.set_title("Monthly Timeline")
        ax.set_ylabel("Message Count")
        ax.set_xlabel("Month") 
        st.pyplot(fig)

        col4, col5 = st.columns(2)
        
        with col4:
            st.title("Most Busy Week Days")
            weekly = df.groupby(['day_name'])['messages'].count().reset_index()
            weekly = weekly.sort_values(by='messages', ascending=False)
            fig, ax = plt.subplots()
            sns.barplot(data=weekly, x='day_name', y='messages', ax=ax, color='orange')
            ax.tick_params(axis='x', rotation=45)
            ax.set_title("Most Busy Week Day")
            ax.set_ylabel("Message Count")
            ax.set_xlabel("Week Day")
            st.pyplot(fig)

        with col5:
            st.title("Top 5 Active Users")
            x = df['users'].value_counts().head(5).reset_index()
            x.columns = ['user', 'message_count']
            fig, ax = plt.subplots()
            sns.barplot(data=x, x='user', y='message_count', color='green', ax=ax)
            ax.set_title('Top 5 Active Users')
            ax.set_xlabel('Most Active Users')
            ax.set_ylabel('Message Count')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        

        st.title('Word Cloud')
        wc = WordCloud(width=400,height=400,min_font_size=10,background_color='white')
        temp1 = df[df['messages']!='<Media omitted>\n']
        # st.dataframe(temp1)
        df_wc = wc.generate(temp1['messages'].str.cat(sep=' '))
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)   

        col6 , col7 = st.columns(2)

        with col6:
            st.title('Chat Contribution Percentage')
            count=df['users'].value_counts()
            percentage = round((df['users'].value_counts()/df.shape[0])*100,1)
            kcount = pd.DataFrame({'Count':count,'Percentage':percentage})
            st.dataframe(kcount)

        with col7:
            st.title('Most Frequent Words')
            temp2 = df[df['messages'] != '<Media omitted>\n']
            temp2 = temp2[temp2['users'] != 'group_notification']
            with open("D:\ML\WhatsApp Message Analayzier\FrontEnd\stop_hinglish.txt", "r") as file:
                stop_words = file.read().splitlines()
            words=[]
            for msg in temp2['messages']:
                for word in msg.lower().split():
                    if word not in stop_words:
                        words.append(word)
            fq_words = pd.DataFrame(Counter(words).most_common(20))
            fq_words.rename(columns={0:'words',1:'count'}, inplace=True)
            st.dataframe(fq_words)

        fq_words = fq_words.sort_values(by='count', ascending=True)
        fig,ax=plt.subplots()
        ax.barh(fq_words['words'],fq_words['count'])
        plt.xticks(rotation='vertical')
        plt.xlabel('Count')
        plt.ylabel('Most Frequent Words')
        st.pyplot(fig)


        st.title('Most Frequent Emojis')
        col8,col9 = st.columns(2)

        with col8:
            emojis=[]
            for a in temp2['messages']:
                for char in a:
                    if emoji.is_emoji(char):
                        emojis.append(char)

            emoji_counter = Counter(emojis)
            count_emojis = pd.DataFrame(emoji_counter.most_common(20))
            count_emojis.rename(columns={0:'emoji',1:'count'},inplace=True)  
            per_emoji = round((count_emojis['count']/count_emojis['count'].sum())*100,1)
            count_emojis['percentage'] = per_emoji
            st.dataframe(count_emojis)

        with col9:
            top_5 = count_emojis.head(5)

            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(
                top_5['count'],
                labels=top_5['emoji'],
                autopct='%1.1f%%',
                startangle=90,
                counterclock=False
            )
            ax.set_title("Top 5 Emoji Usage")
            st.pyplot(fig)




        # st.title('Daily Heatmap Timeline')
        # daily = df.groupby(['day_name','hour','minute'])['messages'].count()
        # st.write(daily)









    #Specific Users


    else:
        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        particular_user = df[df['users'] == selected_user]
        total_messages = particular_user.shape[0]
        total_words= particular_user['messages'].dropna().str.split().str.len().sum()
        media_files= particular_user['messages'].str.contains("<Media omitted>").sum()
        with col1:
            st.header("Total Messages")
            st.header(total_messages)

        with col2:
            st.header("Total Words")
            st.header(total_words)

        with col3:
            st.header("Media Shared")
            st.header(media_files)

        st.title("📈Monthly Timeline")
        monthly = df.groupby(['month','users'])["messages"].count().to_frame().reset_index()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        monthly['month'] = pd.Categorical(monthly['month'], categories=month_order, ordered=True)
        monthly = monthly.sort_values('month') 
        monthly_spu = monthly[monthly['users']==selected_user]
        fig, ax = plt.subplots()
        sns.lineplot(data=monthly_spu, x='month', y='messages', marker='o', ax=ax)
        ax.set_title(f"Monthly Timeline for {selected_user}")
        ax.set_ylabel("Message Count")
        ax.set_xlabel("Month") 
        st.pyplot(fig)     

        col4, col5= st.columns(2)
        
        with col4:
            st.title("📊 Most Busy Week Days")
            weekly = particular_user.groupby(['day_name'])['messages'].count().reset_index()
            weekly = weekly.sort_values(by='messages', ascending=False)
            fig, ax = plt.subplots()
            sns.barplot(data=weekly, x='day_name', y='messages', ax=ax, color='orange')
            ax.tick_params(axis='x', rotation=45)
            ax.set_title("Most Busy Week Day")
            ax.set_ylabel("Message Count")
            ax.set_xlabel("Week Day")
            st.pyplot(fig)
            

        with col5:
            st.title("📊 Most Busy Months")
            months = particular_user.groupby(['month'])['messages'].count().reset_index()
            months = months.sort_values(by='messages',ascending=False)
            # st.dataframe(months)
            fig, ax = plt.subplots()
            sns.barplot(data=months,x='month',y='messages', ax=ax,color='green')
            ax.set_title("Most Busy Months")
            ax.set_ylabel("Message Count")
            ax.set_xlabel("Month")
            st.pyplot(fig)

        st.title('Word Cloud')
        wc = WordCloud(width=400,height=400,min_font_size=10,background_color='white')
        temp1 = particular_user[particular_user['messages']!='<Media omitted>\n']
        # st.dataframe(temp1)
        df_wc = wc.generate(temp1['messages'].str.cat(sep=' '))
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)   

        col6 , col7 = st.columns(2)


        with col6:
            st.title('Chat Contribution Percentage')
            new_df = round((particular_user['users'].value_counts()/particular_user.shape[0])*100,1).reset_index().rename(columns={'count':'message percentage'})
            st.dataframe(new_df)

        with col7:
            st.title('Most Frequent Words')
            temp2 = particular_user[particular_user['messages'] != '<Media omitted>\n']
            temp2 = temp2[temp2['users'] != 'group_notification']
            with open("D:\ML\WhatsApp Message Analayzier\FrontEnd\stop_hinglish.txt", "r") as file:
                stop_words = file.read().splitlines()
            words=[]
            for msg in temp2['messages']:
                for word in msg.lower().split():
                    if word not in stop_words:
                        words.append(word)
            fq_words = pd.DataFrame(Counter(words).most_common(20))
            fq_words.rename(columns={0:'words',1:'count'}, inplace=True)
            st.dataframe(fq_words)
        
        
        fq_words = fq_words.sort_values(by='count', ascending=True)
        fig,ax=plt.subplots()
        ax.barh(fq_words['words'],fq_words['count'])
        plt.xticks(rotation='vertical')
        plt.xlabel('Count')
        plt.ylabel('Most Frequent Words')
        st.pyplot(fig)


        st.title('Most Frequent Emojis')
        col8,col9 = st.columns(2)

        with col8:
            emojis=[]
            for a in temp2['messages']:
                for char in a:
                    if emoji.is_emoji(char):
                        emojis.append(char)

            emoji_counter = Counter(emojis)
            count_emojis = pd.DataFrame(emoji_counter.most_common(20))
            count_emojis.rename(columns={0:'emoji',1:'count'},inplace=True)  
            per_emoji = round((count_emojis['count']/count_emojis['count'].sum())*100,1)
            count_emojis['percentage'] = per_emoji
            st.dataframe(count_emojis)

        with col9:
            top_5 = count_emojis.head(5)

            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(
                top_5['count'],
                labels=top_5['emoji'],
                autopct='%1.1f%%',
                startangle=90,
                counterclock=False
            )
            ax.set_title("Top 5 Emoji Usage")
            st.pyplot(fig)


                  



