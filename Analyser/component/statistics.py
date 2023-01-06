from Analyser.logger import logging
from Analyser.exception import AnalyserException
import pandas as pd
import sys
from urlextract import URLExtract
from Analyser.constant import *

extract = URLExtract()

class stats:
    def __init__(self, selected_user: str, df: pd.DataFrame):
        try:
            logging.info(f"{'>>'*20} Stats Fetching Log Started {'<<'*20} ")
            self.selected_user = selected_user
            self.df = df

        except Exception as e:
            raise AnalyserException(e,sys)


    def fetch_stats(self):
        try:
            logging.info("********** Fetching Stats **********")

            if self.selected_user != OVERALL_ANALYSIS_KEY:
                df = self.df[self.df[DF_USER_KEY] == self.selected_user]
            else:
                df = self.df

            # fetching number of messages sent
            num_messages = df.shape[0]
            logging.info(f"num_messages : {num_messages}")

            # fetching number of words sent
            words = []
            for message in df[DF_MESSAGE_KEY]:
                words.extend(message.split(" "))

            logging.info(f"words : {words}")

            # fetching number of media messages
            num_media_messages = df[df[DF_MESSAGE_KEY] == '<Media omitted>\n'].shape[0]

            logging.info(f"num_media_messages : {num_media_messages}")

            # fetching number of links shared
            links = []
            for message in df[DF_MESSAGE_KEY]:
                links.extend(extract.find_urls(message))

            logging.info(f"links : {links}")

            logging.info("********** Fetched Successfully **********")

            return num_messages, len(words), num_media_messages, len(links)

        except Exception as e:
            raise AnalyserException(e,sys)


    def fetch_most_active_user(self):
        try:
            logging.info("********** Fetching most active user **********")

            df_user_percent = round((self.df[DF_USER_KEY].value_counts() / self.df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'User', 'user': 'Percent'})
        
            logging.info("********** Fetched Successfully **********")

            return self.df[DF_USER_KEY].value_counts().head(), df_user_percent

        except Exception as e:
            raise AnalyserException(e,sys)
    